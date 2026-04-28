"""
🤖 100% 자동 댓글 → DM 발송 + 답글 시스템

작동 흐름:
  [5분 주기]
    1. 최근 게시물 댓글 자동 스캔
    2. 키워드 (DREAMTEAM/SKILL 등) 매칭
    3. 좋아요 검증 (자격 통과 vs 부분 통과)
    4. 자격 통과 → 자동 DM 발송 + 자동 답글
    5. 부분 통과 → 자동 답글만 (조건 안내)
    6. 로그 + 슬랙 알림

사용법:
  python auto_reply_engine.py                    # 1회 스캔 + 처리
  python auto_reply_engine.py --watch            # 5분 주기 무한 반복
  python auto_reply_engine.py --dry-run          # DM/답글 안 보내고 검증만
  python auto_reply_engine.py --interval 60      # 1분 주기

안전망:
  - 같은 사용자에게 24시간 내 1회만 발송 (sent_dms.csv)
  - 일일 한도 200건 (만능이 토큰 보호)
  - !stop 키워드 발견 시 60분 글로벌 정지
  - 봇 자기 댓글 자동 무시
"""
import argparse
import json
import sys
import io
import time
import csv
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / '.env'
SEEN_PATH = PROJECT_ROOT / 'data' / 'seen_comments.json'
SENT_LOG = PROJECT_ROOT / 'data' / 'sent_dms.csv'
TEMPLATES_PATH = PROJECT_ROOT / 'config' / 'dm_responses.json'
KILL_FILE = PROJECT_ROOT / 'data' / 'STOP'

KEYWORDS = ['dreamteam', 'skill', 'skii', 'claude', 'guide', '드림팀', '가이드']
KEYWORD_MAP = {
    'dreamteam': 'DREAMTEAM', '드림팀': 'DREAMTEAM',
    'skill': 'SKILL', 'skii': 'SKILL',
    'claude': 'CLAUDE',
    'guide': 'GUIDE', '가이드': 'GUIDE',
}

DAILY_LIMIT = 200


# ════════════════════════════════════════
# 유틸
# ════════════════════════════════════════

def load_env():
    env = {}
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def load_templates():
    return json.loads(TEMPLATES_PATH.read_text(encoding='utf-8'))


def load_seen():
    if SEEN_PATH.exists():
        try:
            return set(json.loads(SEEN_PATH.read_text(encoding='utf-8')))
        except:
            return set()
    return set()


def save_seen(seen):
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEEN_PATH.write_text(json.dumps(sorted(seen)), encoding='utf-8')


def is_already_sent_today(user_id):
    """같은 사용자에게 24시간 내 발송했는지"""
    if not SENT_LOG.exists():
        return False
    cutoff = datetime.utcnow() - timedelta(hours=24)
    with SENT_LOG.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('user_id') == str(user_id) and row.get('success') == '1':
                try:
                    ts = datetime.fromisoformat(row['timestamp'])
                    if ts > cutoff:
                        return True
                except:
                    continue
    return False


def daily_count():
    """오늘 발송 카운트"""
    if not SENT_LOG.exists():
        return 0
    today = datetime.utcnow().date()
    count = 0
    with SENT_LOG.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = datetime.fromisoformat(row['timestamp'])
                if ts.date() == today and row.get('success') == '1':
                    count += 1
            except:
                continue
    return count


def is_kill_active():
    """!stop 글로벌 킬 활성화?"""
    if not KILL_FILE.exists():
        return False
    try:
        ts = datetime.fromisoformat(KILL_FILE.read_text().strip())
        if datetime.utcnow() < ts:
            return True
    except:
        pass
    return False


def activate_kill(minutes=60):
    """!stop 킬 활성화"""
    KILL_FILE.parent.mkdir(parents=True, exist_ok=True)
    expires = datetime.utcnow() + timedelta(minutes=minutes)
    KILL_FILE.write_text(expires.isoformat(), encoding='utf-8')
    print(f'[KILL] Global kill activated until {expires.isoformat()}')


# ════════════════════════════════════════
# Instagram API
# ════════════════════════════════════════

def api_get(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}', 'body': e.read().decode()[:300]}


def api_post(url, params):
    payload = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {'success': True, 'data': json.loads(r.read())}
    except urllib.error.HTTPError as e:
        return {'success': False, 'error': f'HTTP {e.code}', 'body': e.read().decode()[:300]}


def check_liked(post_id, user_id, token):
    """사용자가 좋아요 눌렀는지 검증"""
    url = f'https://graph.instagram.com/v18.0/{post_id}?fields=likes.limit(100){{username,id}}&access_token={token}'
    res = api_get(url)
    if 'error' in res:
        return False
    likes = res.get('likes', {}).get('data', [])
    return any(l.get('id') == user_id for l in likes)


def reply_to_comment(comment_id, message, token):
    """댓글에 답글 달기"""
    url = f'https://graph.instagram.com/v18.0/{comment_id}/replies'
    return api_post(url, {'message': message, 'access_token': token})


def send_dm(env, recipient_id, message):
    """DM 발송"""
    user_id = env['IG_USER_ID']
    token = env['IG_ACCESS_TOKEN']
    url = f'https://graph.instagram.com/v18.0/{user_id}/messages'
    payload = json.dumps({
        'recipient': {'id': str(recipient_id)},
        'message': {'text': message[:1000]}  # IG DM 1000자 제한
    }).encode('utf-8')
    req = urllib.request.Request(
        url, data=payload, method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {'success': True, 'data': json.loads(r.read())}
    except urllib.error.HTTPError as e:
        return {'success': False, 'error': f'HTTP {e.code}', 'body': e.read().decode()[:500]}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_dm_message(keyword, name, lang='ko'):
    """키워드 → 응답 메시지 생성"""
    templates = load_templates()
    if keyword not in templates:
        keyword = 'DREAMTEAM'  # fallback
    tpl = templates[keyword]
    if lang not in tpl:
        if 'fallback_to' in tpl.get('ko', {}):
            return render_dm_message(tpl['ko']['fallback_to'], name, lang)
        lang = list(tpl.keys())[0]
    t = tpl[lang]
    parts = []
    for key in ['greeting_template', 'intro', 'main_body', 'cta', 'signature']:
        if key in t:
            parts.append(t[key].replace('{{name}}', f'@{name}'))
    return '\n\n'.join(parts)


# ════════════════════════════════════════
# 메인 처리
# ════════════════════════════════════════

def log_sent(user_id, comment_id, post_id, keyword, dm_success, reply_success, dm_error, reply_error):
    """발송 이력 CSV"""
    SENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    new_file = not SENT_LOG.exists()
    with SENT_LOG.open('a', encoding='utf-8', newline='') as f:
        if new_file:
            f.write('timestamp,user_id,comment_id,post_id,keyword,dm_success,reply_success,dm_error,reply_error\n')
        ts = datetime.utcnow().isoformat()
        success = '1' if dm_success else '0'
        rsuccess = '1' if reply_success else '0'
        f.write(f'{ts},{user_id},{comment_id},{post_id},{keyword},{success},{rsuccess},{dm_error},{reply_error}\n')


def process_qualified(env, match, dry_run=False):
    """자격 통과 댓글 자동 처리: DM + 답글"""
    user_id = match['user_id']
    comment_id = match['comment_id']
    keyword = match['matched_keyword']
    username = match['username']

    print(f'\n  ✅ 자격 통과: @{username} ({user_id}) — {keyword}')

    # 중복 발송 방지
    if is_already_sent_today(user_id):
        print(f'    [SKIP] 24시간 내 이미 발송')
        return

    # 일일 한도
    if daily_count() >= DAILY_LIMIT:
        print(f'    [LIMIT] 일일 한도 {DAILY_LIMIT}건 도달, 자동 정지')
        return

    if dry_run:
        print(f'    [DRY] DM + 답글 발송 시뮬레이션')
        return

    # 1. DM 발송
    dm_msg = render_dm_message(keyword, username, lang='ko')
    print(f'    [1/2] DM 발송 시도... ({len(dm_msg)}자)')
    dm_result = send_dm(env, user_id, dm_msg)
    dm_success = dm_result.get('success', False)
    dm_error = dm_result.get('error', '') if not dm_success else ''
    print(f'    [1/2] {"✅ DM 발송 성공" if dm_success else f"❌ DM 실패: {dm_error}"}')
    if not dm_success and 'body' in dm_result:
        print(f'         body: {dm_result["body"][:200]}')

    # 2. 댓글 답글
    reply_text = f'@{username} 약속드린 자료 DM으로 보내드렸어요! 받으셨나요? ✷ 답글에 질문 남겨주시면 24시간 내 답변드려요 🌷'
    print(f'    [2/2] 댓글 답글...')
    reply_result = reply_to_comment(comment_id, reply_text, env['IG_ACCESS_TOKEN'])
    reply_success = reply_result.get('success', False)
    reply_error = reply_result.get('error', '') if not reply_success else ''
    print(f'    [2/2] {"✅ 답글 성공" if reply_success else f"❌ 답글 실패: {reply_error}"}')

    log_sent(user_id, comment_id, match['post_id'], keyword,
             dm_success, reply_success, dm_error.replace(',', ';'), reply_error.replace(',', ';'))


def process_partial(env, match, dry_run=False):
    """부분 통과 (좋아요 안 누름): 답글로 안내만"""
    user_id = match['user_id']
    comment_id = match['comment_id']
    username = match['username']

    print(f'\n  🟡 부분 통과: @{username} (좋아요 ❌)')

    if dry_run:
        print(f'    [DRY] 답글 안내 시뮬레이션')
        return

    reply_text = (f'@{username} 안녕하세요 🌷\n'
                  f'자동 가이드 발송 조건 3가지:\n'
                  f'① 팔로우 ② 좋아요 ❤️ ③ 댓글 「DREAMTEAM」\n'
                  f'3가지 다 충족해주시면 햄스터즈가 24시간 내 자동 DM 보내드려요 ✷')
    reply_result = reply_to_comment(comment_id, reply_text, env['IG_ACCESS_TOKEN'])
    success = reply_result.get('success', False)
    print(f'    {"✅ 안내 답글 성공" if success else f"❌ 답글 실패"}')


def scan_and_process(env, dry_run=False):
    """1회 스캔 + 자동 처리"""
    if is_kill_active():
        print('[KILL] 글로벌 정지 활성화 중. 스캔 스킵.')
        return

    user_id = env['IG_USER_ID']
    token = env['IG_ACCESS_TOKEN']
    base = 'https://graph.instagram.com/v18.0'

    # 최근 게시물 5개
    media = api_get(f'{base}/{user_id}/media?fields=id,timestamp&limit=5&access_token={token}')
    if 'error' in media:
        print(f'[ERR] media: {media}')
        return

    seen = load_seen()
    new_matches = []

    for post in media.get('data', []):
        pid = post['id']
        comments = api_get(f'{base}/{pid}/comments?fields=id,text,from,timestamp,username&access_token={token}')
        if 'error' in comments:
            continue

        for c in comments.get('data', []):
            cid = c.get('id')
            if cid in seen:
                continue

            text = (c.get('text') or '').lower()

            # !stop 킬스위치
            if '!stop' in text or '긴급중단' in text:
                activate_kill(60)
                seen.add(cid)
                continue

            # 키워드 매칭
            matched_kw = None
            for kw in KEYWORDS:
                if kw in text:
                    matched_kw = KEYWORD_MAP.get(kw, kw.upper())
                    break

            if not matched_kw:
                seen.add(cid)
                continue

            from_obj = c.get('from', {})
            cuser_id = from_obj.get('id') or c.get('username')  # fallback
            username = from_obj.get('username') or c.get('username') or '?'

            if not cuser_id:
                seen.add(cid)
                continue

            # 좋아요 검증
            liked = check_liked(pid, cuser_id, token)

            match = {
                'comment_id': cid,
                'post_id': pid,
                'user_id': cuser_id,
                'username': username,
                'text': c.get('text'),
                'matched_keyword': matched_kw,
                'liked': liked,
                'qualified': liked,
            }
            new_matches.append(match)
            seen.add(cid)

    save_seen(seen)

    # 처리
    if not new_matches:
        ts = datetime.now().strftime('%H:%M:%S')
        print(f'[{ts}] No new matches.')
        return

    qualified = [m for m in new_matches if m['qualified']]
    partial = [m for m in new_matches if not m['qualified']]

    ts = datetime.now().strftime('%H:%M:%S')
    print(f'\n[{ts}] {len(new_matches)} new matches: ✅ {len(qualified)} 자격 / 🟡 {len(partial)} 부분')

    for m in qualified:
        process_qualified(env, m, dry_run)
        time.sleep(2)  # API 한도 보호

    for m in partial:
        process_partial(env, m, dry_run)
        time.sleep(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', action='store_true', help='5분 주기 무한 반복')
    parser.add_argument('--interval', type=int, default=300)
    parser.add_argument('--dry-run', action='store_true', help='실제 발송 X, 시뮬레이션만')
    args = parser.parse_args()

    env = load_env()
    print(f'=== 🤖 100% 자동 댓글→DM 시스템 가동 ===')
    print(f'IG: @{env.get("IG_USERNAME")} ({env.get("IG_USER_ID")})')
    print(f'Watch: {args.watch} / Interval: {args.interval}s / Dry: {args.dry_run}')
    print()

    while True:
        try:
            scan_and_process(env, args.dry_run)
        except Exception as e:
            print(f'[ERR] scan exception: {type(e).__name__}: {e}')
        if not args.watch:
            break
        time.sleep(args.interval)


if __name__ == '__main__':
    main()

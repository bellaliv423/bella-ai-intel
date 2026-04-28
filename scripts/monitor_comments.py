"""
인스타 댓글 모니터링 + 슬랙 알림 (햄스터즈 자동 응답 코드 가동 전 임시 브리지)

사용법:
  python monitor_comments.py                  # 1회 스캔
  python monitor_comments.py --watch           # 5분마다 반복 (Ctrl+C 종료)
  python monitor_comments.py --post-id <ID>    # 특정 게시물만

흐름:
  1. 최근 5개 게시물의 댓글 조회
  2. DREAMTEAM/SKILL/CLAUDE/GUIDE 키워드 매칭
  3. 슬랙 #bella-ceo 알림 → 벨라님이 send_dm_manual.py로 1줄 답장
  4. 자동 시스템 가동 후 본 모듈은 webhook 트리거로 대체
"""
import argparse
import json
import sys
import io
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / '.env'
SEEN_PATH = PROJECT_ROOT / 'data' / 'seen_comments.json'

KEYWORDS = ['dreamteam', 'skill', 'skii', 'claude', 'guide', '드림팀', '가이드']


def load_env():
    env = {}
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def load_seen():
    if SEEN_PATH.exists():
        return set(json.loads(SEEN_PATH.read_text(encoding='utf-8')))
    return set()


def save_seen(seen: set):
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEEN_PATH.write_text(json.dumps(sorted(seen)), encoding='utf-8')


def api_get(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {'error': f'HTTP {e.code}', 'body': body[:300]}


def check_liked(post_id: str, user_id: str, token: str) -> bool:
    """
    좋아요 검증 — 사용자가 게시물에 좋아요 눌렀는지 확인
    Instagram Graph API: GET /{post_id}?fields=likes
    팔로우 검증은 인스타 자체 정책으로 DM 시점에 자동 필터링
    (미팔로워는 메시지 요청 폴더로 들어가서 사용자 거절 가능)
    """
    url = f'https://graph.instagram.com/v18.0/{post_id}?fields=likes.limit(100){{username,id}}&access_token={token}'
    res = api_get(url)
    if 'error' in res:
        # API 에러 시 보수적으로 False (DM 안 보냄, 슬랙 알림으로 벨라님 수동 처리)
        return False
    likes = res.get('likes', {}).get('data', [])
    return any(like.get('id') == user_id for like in likes)


def scan(env: dict, target_post_id: str = None, seen: set = None) -> list:
    if seen is None:
        seen = set()

    user_id = env['IG_USER_ID']
    token = env['IG_ACCESS_TOKEN']
    base = f'https://graph.instagram.com/v18.0'

    if target_post_id:
        post_ids = [target_post_id]
    else:
        media = api_get(f'{base}/{user_id}/media?fields=id,timestamp,caption&limit=5&access_token={token}')
        if 'error' in media:
            print(f'[ERR] media fetch: {media}')
            return []
        post_ids = [m['id'] for m in media.get('data', [])]

    matches = []
    for pid in post_ids:
        comments = api_get(f'{base}/{pid}/comments?fields=id,text,from,timestamp&access_token={token}')
        if 'error' in comments:
            print(f'[WARN] comments fetch failed for {pid}: {comments}')
            continue

        for c in comments.get('data', []):
            cid = c.get('id')
            if cid in seen:
                continue
            text = (c.get('text') or '').lower()
            for kw in KEYWORDS:
                if kw in text:
                    cuser_id = c.get('from', {}).get('id')
                    # 좋아요 검증
                    liked = check_liked(pid, cuser_id, token) if cuser_id else False
                    matches.append({
                        'comment_id': cid,
                        'post_id': pid,
                        'user_id': cuser_id,
                        'username': c.get('from', {}).get('username', '?'),
                        'text': c.get('text'),
                        'matched_keyword': kw.upper(),
                        'timestamp': c.get('timestamp'),
                        'liked': liked,
                        'qualified': liked  # 댓글 + 좋아요 둘 다 = 자격 통과
                    })
                    seen.add(cid)
                    break
    return matches


def slack_alert(env: dict, matches: list):
    """슬랙 #bella-ceo 알림 — 자격 통과(댓글+좋아요) vs 부분 통과 분리 표시"""
    webhook = env.get('SLACK_WEBHOOK_BELLA_CEO', '')
    if not webhook or not matches:
        return

    qualified = [m for m in matches if m.get('qualified')]
    partial = [m for m in matches if not m.get('qualified')]

    lines = []
    lines.append(f'🚨 *댓글 키워드 매칭 {len(matches)}건* — 자격 통과 {len(qualified)} / 부분 {len(partial)}\n')

    if qualified:
        lines.append('━━━ ✅ *자격 통과 (댓글 + 좋아요)* — 즉시 DM 발송 ━━━')
        for m in qualified:
            lines.append(
                f'• *{m["matched_keyword"]}* by @{m["username"]} '
                f'(user_id: `{m["user_id"]}`)\n'
                f'  댓글: "{m["text"]}"\n'
                f'  ✅ 좋아요 OK\n'
                f'  → `python scripts/send_dm_manual.py --user {m["user_id"]} '
                f'--keyword {m["matched_keyword"]} --name @{m["username"]}`'
            )

    if partial:
        lines.append('\n━━━ 🟡 *부분 통과 (댓글만, 좋아요 없음)* — 답글 유도 ━━━')
        for m in partial:
            lines.append(
                f'• *{m["matched_keyword"]}* by @{m["username"]} '
                f'(user_id: `{m["user_id"]}`)\n'
                f'  댓글: "{m["text"]}"\n'
                f'  ❌ 좋아요 안 누름 → 답글: "팔로우+좋아요 부탁드려요🌷 그러면 가이드 자동 발송!"'
            )

    msg = '\n'.join(lines)

    payload = json.dumps({'text': msg}).encode('utf-8')
    try:
        req = urllib.request.Request(webhook, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        print(f'[SLACK] Alerted (qualified={len(qualified)}, partial={len(partial)})')
    except Exception as e:
        print(f'[SLACK] Failed: {e}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', action='store_true', help='Loop every 5 min')
    parser.add_argument('--post-id', help='Scan specific post only')
    parser.add_argument('--interval', type=int, default=300, help='Watch interval seconds (default 300)')
    args = parser.parse_args()

    env = load_env()

    while True:
        seen = load_seen()
        ts = datetime.now().strftime('%H:%M:%S')
        print(f'[{ts}] Scanning...')
        matches = scan(env, args.post_id, seen)
        if matches:
            print(f'[{ts}] {len(matches)} new keyword matches!')
            for m in matches:
                print(f'  - {m["matched_keyword"]} by @{m["username"]}: "{m["text"]}"')
            slack_alert(env, matches)
            save_seen(seen)
        else:
            print(f'[{ts}] No new keyword matches.')

        if not args.watch:
            break
        time.sleep(args.interval)


if __name__ == '__main__':
    main()

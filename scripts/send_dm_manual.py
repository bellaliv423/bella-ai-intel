"""
수동 DM 발송 스크립트 (햄스터즈 자동 시스템 가동 전 임시용)

사용법:
  python send_dm_manual.py --user <USER_ID> --keyword DREAMTEAM
  python send_dm_manual.py --user <USER_ID> --keyword SKILL
  python send_dm_manual.py --user <USER_ID> --custom "안녕하세요..."

발행 후 댓글 받으면 → 본 스크립트로 즉시 DM 발송
나중에 햄스터즈 자동 시스템 (auto_comment_to_dm.py) 가동 시 본 로직 통합
"""
import argparse
import json
import sys
import io
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / '.env'
TEMPLATES_PATH = PROJECT_ROOT / 'config' / 'dm_responses.json'
LOG_PATH = PROJECT_ROOT / 'data' / 'sent_dms.csv'


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


def render_message(keyword: str, name: str, lang: str = 'ko') -> str:
    templates = load_templates()
    if keyword not in templates:
        keyword = 'default_unknown'

    tpl = templates[keyword]
    if lang not in tpl:
        if 'fallback_to' in tpl.get('ko', {}):
            return render_message(tpl['ko']['fallback_to'], name, lang)
        lang = list(tpl.keys())[0]

    t = tpl[lang]
    parts = []
    if 'greeting_template' in t:
        parts.append(t['greeting_template'].replace('{{name}}', name))
    if 'intro' in t:
        parts.append(t['intro'])
    if 'main_body' in t:
        parts.append(t['main_body'])
    if 'cta' in t:
        parts.append(t['cta'])
    if 'signature' in t:
        parts.append(t['signature'])
    return '\n\n'.join(parts)


def send_ig_dm(env: dict, recipient_id: str, message: str) -> dict:
    ig_user_id = env['IG_USER_ID']
    token = env['IG_ACCESS_TOKEN']
    url = f'https://graph.instagram.com/v18.0/{ig_user_id}/messages'
    payload = json.dumps({
        'recipient': {'id': recipient_id},
        'message': {'text': message}
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {'success': True, 'response': json.loads(r.read())}
    except urllib.error.HTTPError as e:
        return {'success': False, 'error': f'HTTP {e.code}', 'body': e.read().decode()}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def log_sent(user_id: str, keyword: str, message: str, result: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_file = not LOG_PATH.exists()
    with LOG_PATH.open('a', encoding='utf-8') as f:
        if new_file:
            f.write('timestamp,user_id,keyword,success,error,message_preview\n')
        ts = datetime.utcnow().isoformat()
        success = '1' if result.get('success') else '0'
        error = result.get('error', '').replace(',', ';')
        preview = message[:80].replace('\n', ' ').replace(',', ';')
        f.write(f'{ts},{user_id},{keyword},{success},{error},{preview}\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True, help='Recipient IG user ID')
    parser.add_argument('--keyword', default='DREAMTEAM', choices=['DREAMTEAM', 'SKILL', 'CLAUDE', 'GUIDE'])
    parser.add_argument('--name', default='친구')
    parser.add_argument('--lang', default='ko', choices=['ko', 'zh', 'en'])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--custom', help='Override with custom message')
    args = parser.parse_args()

    env = load_env()
    msg = args.custom or render_message(args.keyword, args.name, args.lang)

    print('=== DM Preview ===')
    print(f'Recipient: {args.user}')
    print(f'Keyword: {args.keyword}')
    print(f'Lang: {args.lang}')
    print(f'Length: {len(msg)} chars')
    print('---')
    print(msg)
    print('---')

    if args.dry_run:
        print('[DRY RUN] Not sent.')
        return

    print('Sending...')
    result = send_ig_dm(env, args.user, msg)
    log_sent(args.user, args.keyword, msg, result)

    if result['success']:
        print(f'[OK] Sent. Response: {result["response"]}')
    else:
        print(f'[FAIL] {result["error"]}')
        if 'body' in result:
            print(f'Body: {result["body"][:300]}')


if __name__ == '__main__':
    main()

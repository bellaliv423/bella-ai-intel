"""
인스타 캐러셀 발행 (3단계: 컨테이너 N개 → 캐러셀 묶기 → 게시)

사용법:
  python publish_carousel.py --config publish_vol001_ko.json
  python publish_carousel.py --config publish_vol001_ko.json --dry-run

작동 원리:
  1. 각 이미지 URL → POST /{IG}/media (image_url + is_carousel_item=true) → container_id
  2. 모든 container_id 모아 → POST /{IG}/media (media_type=CAROUSEL, children=...) → carousel_id
  3. POST /{IG}/media_publish (creation_id=carousel_id) → post_id
"""
import argparse
import json
import sys
import io
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / '.env'


def load_env():
    env = {}
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def api_post(url: str, params: dict) -> dict:
    payload = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return {'success': True, 'data': json.loads(r.read())}
    except urllib.error.HTTPError as e:
        return {'success': False, 'error': f'HTTP {e.code}', 'body': e.read().decode()[:500]}
    except Exception as e:
        return {'success': False, 'error': f'{type(e).__name__}: {e}'}


def api_get(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}', 'body': e.read().decode()[:500]}


def wait_container_ready(env, container_id, max_attempts=15):
    """컨테이너 처리 대기 (Instagram 서버가 이미지 다운로드+검증)"""
    token = env['IG_ACCESS_TOKEN']
    for i in range(max_attempts):
        url = f'https://graph.instagram.com/v18.0/{container_id}?fields=status_code&access_token={token}'
        res = api_get(url)
        status = res.get('status_code', '?')
        print(f'    [{i+1}/{max_attempts}] container {container_id} status: {status}')
        if status == 'FINISHED':
            return True
        if status == 'ERROR':
            return False
        time.sleep(3)
    return False


def publish(config_path, dry_run=False):
    env = load_env()
    ig_user_id = env['IG_USER_ID']
    token = env['IG_ACCESS_TOKEN']
    base = f'https://graph.instagram.com/v18.0'

    cfg = json.loads(Path(config_path).read_text(encoding='utf-8'))
    image_urls = cfg['image_urls']
    caption = cfg['caption']

    print(f'=== Publish Plan ===')
    print(f'IG User: {env.get("IG_USERNAME")} ({ig_user_id})')
    print(f'Slides: {len(image_urls)}')
    for i, u in enumerate(image_urls, 1):
        print(f'  {i}. {u}')
    print(f'Caption length: {len(caption)} chars')
    print(f'Caption preview: {caption[:200]}...')
    print()

    if dry_run:
        print('[DRY RUN] Stopping before any API call.')
        return

    # Step 1: 각 이미지 컨테이너 생성
    print('=== Step 1: Create item containers ===')
    container_ids = []
    for i, img_url in enumerate(image_urls, 1):
        print(f'  Creating container {i}/{len(image_urls)}...')
        res = api_post(f'{base}/{ig_user_id}/media', {
            'image_url': img_url,
            'is_carousel_item': 'true',
            'access_token': token,
        })
        if not res['success']:
            print(f'  [FAIL] {res}')
            return
        cid = res['data']['id']
        container_ids.append(cid)
        print(f'  [OK] container_id={cid}')
        # 이미지 처리 대기
        if not wait_container_ready(env, cid):
            print(f'  [WARN] container {cid} not FINISHED, continuing...')

    # Step 2: 캐러셀 묶기
    print('\n=== Step 2: Create carousel container ===')
    res = api_post(f'{base}/{ig_user_id}/media', {
        'media_type': 'CAROUSEL',
        'children': ','.join(container_ids),
        'caption': caption,
        'access_token': token,
    })
    if not res['success']:
        print(f'[FAIL] {res}')
        return
    carousel_id = res['data']['id']
    print(f'[OK] carousel_id={carousel_id}')

    # 캐러셀도 처리 대기
    print('\n=== Waiting for carousel to be ready ===')
    if not wait_container_ready(env, carousel_id, max_attempts=20):
        print('[WARN] Carousel not FINISHED, attempting publish anyway...')

    # Step 3: 게시
    print('\n=== Step 3: Publish ===')
    res = api_post(f'{base}/{ig_user_id}/media_publish', {
        'creation_id': carousel_id,
        'access_token': token,
    })
    if not res['success']:
        print(f'[FAIL] {res}')
        return
    post_id = res['data']['id']
    print(f'\n🎉 [PUBLISHED] post_id={post_id}')

    # 영구 링크 조회
    permalink_res = api_get(f'{base}/{post_id}?fields=permalink,timestamp&access_token={token}')
    print(f'\nPermalink: {permalink_res.get("permalink")}')
    print(f'Timestamp: {permalink_res.get("timestamp")}')

    # 결과 저장
    log = {
        'published_at': datetime.utcnow().isoformat(),
        'post_id': post_id,
        'carousel_id': carousel_id,
        'container_ids': container_ids,
        'permalink': permalink_res.get('permalink'),
        'caption_length': len(caption),
        'config': str(config_path),
    }
    log_path = PROJECT_ROOT / 'data' / f'published_{post_id}.json'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nLog saved: {log_path}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='JSON config file path')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    publish(args.config, args.dry_run)


if __name__ == '__main__':
    main()

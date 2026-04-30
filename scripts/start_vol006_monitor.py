"""Start Upload-Post monitor for VOL.006 KO/EN post"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

ENV = {}
for line in Path("D:/bella-ai-intel/.env").read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        ENV[k.strip()] = v.strip()

API_KEY = ENV["UPLOAD_POST_API_KEY"]
PROFILE = ENV["UPLOAD_POST_PROFILE"]

reply_message_ko = """안녕하세요 ✷

@bella_ai_auto VOL.006 「DREAMTEAM」 댓글 감사해요!

오늘 VOL.006 라이브러리 보내드려요 👇
https://bella-nest.vercel.app/journey/vol-006

Custom Skill 5분 만들기 (목 튜토리얼)
• STEP 1: ~/.claude/skills/myskill/ 폴더 (1분)
• STEP 2: SKILL.md 1개 파일 (3분)
• STEP 3: /myskill 호출 (1분)
• 드림팀 운영 중인 10+ Skill 사례 포함

매일 다른 VOL · 매일 새로운 가치 (중복 0%)
이전 VOL: https://bella-nest.vercel.app/journey

팔로우 + 알림 ON 부탁드려요!
— 윈디 ✷"""

reply_message_en = """Hi ✷

Thanks for your 'DREAMTEAM' comment on @bella_ai_auto VOL.006!

Today's library 👇
https://bella-nest.vercel.app/journey/vol-006

Custom Skill in 5 minutes (Thursday Tutorial)
- STEP 1: ~/.claude/skills/myskill/ folder (1 min)
- STEP 2: 1 SKILL.md file (3 min)
- STEP 3: Call /myskill (1 min)
- Dream Team's 10+ skills in production

Different VOL daily · Fresh value (0% repeat)
Past VOLs: https://bella-nest.vercel.app/journey

Follow + Notifications ON!
- Windy ✷"""

LANG = sys.argv[1] if len(sys.argv) > 1 else "ko"
POST_URL = sys.argv[2] if len(sys.argv) > 2 else None

if not POST_URL:
    print("Usage: python start_vol006_monitor.py [ko|en] <POST_URL>")
    print("Example: python start_vol006_monitor.py ko https://www.instagram.com/p/XXXX/")
    sys.exit(1)

reply_message = reply_message_en if LANG == "en" else reply_message_ko

payload = {
    "post_url": POST_URL,
    "reply_message": reply_message,
    "profile_username": PROFILE,
    "monitoring_interval": 15,
    "trigger_keywords": ["DREAMTEAM", "드림팀", "dream team"]
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    "https://api.upload-post.com/api/uploadposts/autodms/start",
    data=data,
    method="POST",
    headers={
        "Authorization": f"Apikey {API_KEY}",
        "Content-Type": "application/json",
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode()
        print("OK:", body)
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}:", e.read().decode()[:500])
except Exception as e:
    print(f"ERR {type(e).__name__}:", e)

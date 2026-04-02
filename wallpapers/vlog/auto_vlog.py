"""
Dream Team Vlog 자동 생성 + 둥지 갤러리 업데이트
- Task Scheduler로 주 3회 (화/목/토 11:00) 자동 실행
- 에피소드 데이터 → HTML 생성 → PNG export → gallery.json 업데이트
"""
import json
import os
import random
from datetime import datetime
from playwright.sync_api import sync_playwright

VLOG_DIR = os.path.dirname(os.path.abspath(__file__))
WALL_DIR = os.path.dirname(VLOG_DIR)
NEST_DIR = "D:/bella-nest"
GALLERY_JSON = os.path.join(NEST_DIR, "src/data/gallery.json")
GALLERY_PUBLIC = os.path.join(NEST_DIR, "public/gallery")

# ─── 에피소드 데이터 (자동 순환!) ───
EPISODES = [
    {
        "id": "ep02", "character": "windy", "team": "hamsterz",
        "title": {"ko": "EP02: 윈디의 전략 회의", "zh": "EP02: Windy 的策略會議", "en": "EP02: Windy's Strategy Session"},
        "caption": {"ko": "안경을 올리며 SWOT 분석 시작. 사실 안경 없이도 잘 보여요.", "zh": "推推眼鏡開始SWOT分析。其實不戴眼鏡也看得很清楚。", "en": "Pushing up glasses for SWOT analysis. Actually sees fine without them."},
        "bubble": '"Let me analyze this...\nSWOT first, action second.\n<span style=\"color:#5B8DEF\">This direction is better.</span>"',
        "checklist": ["[x] Market research", "[x] Competitor analysis", "[>] SWOT matrix", "[ ] Strategy deck", "[ ] Bella review"],
        "scene_color": "#5B8DEF",
    },
    {
        "id": "ep03", "character": "robo", "team": "hamsterz",
        "title": {"ko": "EP03: 로보의 코딩 올나잇", "zh": "EP03: Robo 的通宵寫程式", "en": "EP03: Robo's Coding All-Night"},
        "caption": {"ko": "세상에서 제일 작지만 제일 빠른! 빌드 성공 초록불이 최고의 보상.", "zh": "世界上最小但最快！Build成功的綠燈是最好的獎勵。", "en": "Smallest but fastest! Green checkmark is the best reward."},
        "bubble": '"Yes! Building right now!\n3 features done...\n<span style=\"color:#4CAF50\">Build successful!</span>"',
        "checklist": ["[x] npm install", "[x] API endpoint", "[x] UI component", "[>] Build & test", "[ ] Deploy to Vercel"],
        "scene_color": "#4CAF50",
    },
    {
        "id": "ep04", "character": "collie", "team": "puppyz",
        "title": {"ko": "EP04: 콜리 & 시바의 24시간 순찰", "zh": "EP04: Collie & Shiba 的24小時巡邏", "en": "EP04: Collie & Shiba's 24h Patrol"},
        "caption": {"ko": "1시간마다 정확히 순찰! 이상 없으면 '이상 없음!' 보고. 가끔 해바라기 구경도...", "zh": "每小時準時巡邏！沒問題就報告「一切正常！」偶爾也看看向日葵...", "en": "Patrol every hour! 'All clear!' report. Sometimes stops to admire sunflowers..."},
        "bubble": '"All systems nominal!\nHeartbeat: OK\nAPI: responding\n<span style=\"color:#FF9800\">1-hour patrol complete!</span>"',
        "checklist": ["[x] Server health", "[x] API response", "[x] DB connection", "[>] SSL cert check", "[ ] Next patrol: 1hr"],
        "scene_color": "#FF9800",
    },
    {
        "id": "ep05", "character": "panda", "team": "hamsterz",
        "title": {"ko": "EP05: 판다의 사진 촬영 현장", "zh": "EP05: Panda 的攝影現場", "en": "EP05: Panda's Photo Session"},
        "caption": {"ko": "이 각도가 예뻐요! 판다 마킹이 자연산인지 염색인지는 아무도 몰라요.", "zh": "這個角度好美！沒人知道Panda的標記是天然的還是染的。", "en": "This angle is beautiful! Nobody knows if Panda's markings are natural or dyed."},
        "bubble": '"This angle is perfect!\nLighting: golden hour\n<span style=\"color:#607D8B\">One more shot...</span>"',
        "checklist": ["[x] Camera setup", "[x] Lighting check", "[>] Portrait shots", "[ ] Group photo", "[ ] Edit & filter"],
        "scene_color": "#607D8B",
    },
    {
        "id": "ep06", "character": "pomi", "team": "puppyz",
        "title": {"ko": "EP06: 포미의 SNS 포스팅", "zh": "EP06: Pomi 的SNS發文", "en": "EP06: Pomi's SNS Posting"},
        "caption": {"ko": "화려하게 포스팅! 팔로워 수를 매일 밤 확인하는 게 루틴이에요.", "zh": "華麗發文！每晚確認粉絲數是例行公事。", "en": "Post with style! Checking follower count every night is the routine."},
        "bubble": '"Trending hashtags ready!\nCaption: fire emoji x3\n<span style=\"color:#E91E63\">Post it NOW!</span>"',
        "checklist": ["[x] Content ready", "[x] Hashtag research", "[>] Caption writing", "[ ] Schedule post", "[ ] Engagement check"],
        "scene_color": "#E91E63",
    },
    {
        "id": "ep07", "character": "hunter", "team": "hamsterz",
        "title": {"ko": "EP07: 헌터의 버그 사냥 대작전", "zh": "EP07: Hunter 的除蟲大作戰", "en": "EP07: Hunter's Bug Hunt Operation"},
        "caption": {"ko": "...찾았다. 무서운 게 아니라 수줍은 거예요. 어둠 속 하얀 미소가 증거!", "zh": "...找到了。不是可怕，是害羞。黑暗中的白色微笑是證據！", "en": "...Found it. Not scary, just shy. The white smile in the dark is proof!"},
        "bubble": '"...\n...\n<span style=\"color:#EF5350\">...found it.</span>"',
        "checklist": ["[x] Error log scan", "[x] Stack trace", "[>] Root cause", "[ ] Fix & PR", "[ ] Regression test"],
        "scene_color": "#212121",
    },
    {
        "id": "ep08", "character": "all", "team": "both",
        "title": {"ko": "EP08: 전원 회식! 치킨 파티!", "zh": "EP08: 全員聚餐！炸雞派對！", "en": "EP08: Team Dinner! Chicken Party!"},
        "caption": {"ko": "한 주의 마무리는 치킨! 골디가 주문하고, 로보가 배달 추적하고, 도비가 문 지키고.", "zh": "一週的結尾是炸雞！Goldi點餐，Robo追蹤外送，Dobi守門。", "en": "Week ends with chicken! Goldi orders, Robo tracks delivery, Dobi guards the door."},
        "bubble": '"CHICKEN TIME!\nOrder: confirmed\nDelivery: 15 min\n<span style=\"color:#C15F3C\">EVERYONE gather up!</span>"',
        "checklist": ["[x] Order placed", "[x] Delivery tracking", "[>] Table setup", "[ ] Eat eat eat!", "[ ] Food coma..."],
        "scene_color": "#C15F3C",
    },
]

# 현재까지 발행된 에피소드 번호 추적
def get_next_episode():
    """gallery.json에서 마지막 에피소드 번호 확인 후 다음 에피소드 반환"""
    if os.path.exists(GALLERY_JSON):
        with open(GALLERY_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        existing_ids = [v["id"] for v in data.get("vlog", [])]
    else:
        existing_ids = []

    for ep in EPISODES:
        if ep["id"] not in existing_ids:
            return ep

    # 모든 에피소드 소진 → 처음부터 (시즌2 식으로)
    return None


def update_gallery_json(ep):
    """gallery.json의 vlog 배열에 새 에피소드 추가"""
    with open(GALLERY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_entry = {
        "id": ep["id"],
        "src": f"/gallery/{ep['id']}_post_1080x1080.png",
        "storySrc": f"/gallery/{ep['id']}_story_1080x1920.png",
        "title": ep["title"],
        "caption": ep["caption"],
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    data["vlog"].append(new_entry)

    with open(GALLERY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] gallery.json updated with {ep['id']}")


def generate_and_export(ep):
    """HTML 생성 → PNG export → gallery 복사"""
    # EP01은 이미 수동으로 만듬, EP02부터 템플릿으로 자동 생성
    post_html = os.path.join(VLOG_DIR, f"{ep['id']}_post.html")
    story_html = os.path.join(VLOG_DIR, f"{ep['id']}_story.html")

    # TODO: 템플릿 기반 HTML 자동 생성 (Phase 2)
    # 현재는 수동 HTML이 있다고 가정

    if not os.path.exists(post_html):
        print(f"[SKIP] {post_html} not found — create HTML first!")
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Post (1080x1080)
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.goto(f"file:///{post_html}".replace("\\", "/"))
        page.wait_for_timeout(3000)
        post_png = os.path.join(VLOG_DIR, f"{ep['id']}_post_1080x1080.png")
        page.screenshot(path=post_png)
        print(f"[OK] {ep['id']} post exported")

        # Story (1080x1920)
        if os.path.exists(story_html):
            page2 = browser.new_page(viewport={"width": 1080, "height": 1920})
            page2.goto(f"file:///{story_html}".replace("\\", "/"))
            page2.wait_for_timeout(3000)
            story_png = os.path.join(VLOG_DIR, f"{ep['id']}_story_1080x1920.png")
            page2.screenshot(path=story_png)
            print(f"[OK] {ep['id']} story exported")

        browser.close()

    # Copy to bella-nest gallery
    import shutil
    for f in [f"{ep['id']}_post_1080x1080.png", f"{ep['id']}_story_1080x1920.png"]:
        src = os.path.join(VLOG_DIR, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(GALLERY_PUBLIC, f))
            print(f"[OK] Copied to gallery: {f}")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("  Dream Team Vlog Auto Publisher")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    ep = get_next_episode()
    if ep is None:
        print("[INFO] All episodes published! Time for Season 2!")
    else:
        print(f"[NEXT] {ep['id']}: {ep['title']['en']}")
        if generate_and_export(ep):
            update_gallery_json(ep)
            print(f"\n[DONE] {ep['id']} published to bella-nest gallery!")
        else:
            print(f"\n[WAIT] Create HTML for {ep['id']} first, then re-run.")

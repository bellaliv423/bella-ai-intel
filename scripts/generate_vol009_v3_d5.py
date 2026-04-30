"""
VOL.009 D+5 vol001 톤 — 4 KO + 4 EN
주제: Claude Code 옵시디언 + Claude Code 지식관리 (FRAMEWORK+STORY · 강사 아티)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = Path("D:/bella-nest/public/posts/2026-05-04")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"
FONT_ITALIC_EN = "C:/Windows/Fonts/cambriai.ttf"
FONT_BOLD_EN = "C:/Windows/Fonts/cambriab.ttf"

CREAM = "#ede2ce"
TERRA = "#b25d3a"
BLACK = "#1a1814"
GRAY = "#6b6258"
GRAY_LIGHT = "#a8a094"
WHITE = "#ffffff"
PURPLE = "#8b5cf6"
PINK = "#ec4899"
AMBER = "#f59e0b"
GREEN = "#10b981"

W, H = 1080, 1080


def font(size, bold=True, italic=False, en=False):
    if italic and en:
        return ImageFont.truetype(FONT_ITALIC_EN, size)
    if en:
        return ImageFont.truetype(FONT_BOLD_EN if bold else FONT_ITALIC_EN, size)
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def text_size(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text_centered(draw, text, y, font_obj, fill, w=W):
    tw, _ = text_size(draw, text, font_obj)
    draw.text(((w - tw) // 2, y), text, font=font_obj, fill=fill)


def draw_segments(draw, segments, y, w=W, font_obj=None):
    total_w = 0
    for text, _ in segments:
        tw, _h = text_size(draw, text, font_obj)
        total_w += tw
    x = (w - total_w) // 2
    for text, color in segments:
        draw.text((x, y), text, font=font_obj, fill=color)
        tw, _ = text_size(draw, text, font_obj)
        x += tw


def draw_sparkle_4point(draw, cx, cy, r, fill, w_main=4, w_diag=2):
    draw.polygon([(cx - w_main // 2, cy), (cx, cy - r), (cx + w_main // 2, cy), (cx, cy + r)], fill=fill)
    draw.polygon([(cx, cy - w_main // 2), (cx + r, cy), (cx, cy + w_main // 2), (cx - r, cy)], fill=fill)
    s = r // 3
    draw.polygon([(cx - 2, cy - 2), (cx + s, cy - s), (cx + 2, cy + 2), (cx - s, cy + s)], fill=fill)
    draw.polygon([(cx + 2, cy - 2), (cx + s, cy + s), (cx - 2, cy + 2), (cx - s, cy - s)], fill=fill)


def draw_pill_badge(draw, text, x, y, font_obj, padding=(28, 12), fill=TERRA, sparkle=True):
    tw, th = text_size(draw, text, font_obj)
    pad_x, pad_y = padding
    badge_h = th + pad_y * 2 + 6
    spark_w = 30 if sparkle else 0
    badge_w = tw + pad_x * 2 + spark_w
    rect = [x, y, x + badge_w, y + badge_h]
    draw.rounded_rectangle(rect, radius=badge_h // 2, fill=fill)
    draw.text((x + pad_x, y + pad_y), text, font=font_obj, fill=WHITE)
    if sparkle:
        draw_sparkle_4point(draw, x + pad_x + tw + 16, y + badge_h // 2, 8, fill=WHITE)
    return rect[2], rect[3]


def draw_meta_top(draw, left_text, right_badge_text, sparkle=True, y=70):
    f = font(24, bold=True)
    draw.text((60, y + 10), left_text, font=f, fill=BLACK)
    if right_badge_text:
        f_b = font(22, bold=True)
        tw, th = text_size(draw, right_badge_text, f_b)
        spark_w = 30 if sparkle else 0
        badge_w = tw + 56 + spark_w
        bx = W - 60 - badge_w
        draw_pill_badge(draw, right_badge_text, bx, y, f_b, sparkle=sparkle)


def draw_footer(draw, page_num):
    draw.line([(60, H - 70), (W - 60, H - 70)], fill=GRAY_LIGHT, width=1)
    f = font(22, bold=True)
    text = f"{page_num}/4 · @bella_ai_auto"
    tw, th = text_size(draw, text, f)
    draw.text((W - 60 - tw, H - 50), text, font=f, fill=GRAY)


# ==================== KO ====================

def slide_ko_1():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "VOL.009 — 2026.05.02 · MONDAY", "D+12", sparkle=True)

    f_head = font(94, bold=True)
    line_h = 116

    y = 250
    seg1 = [("내 ", BLACK), ("두 번째 뇌", TERRA)]
    draw_segments(draw, seg1, y, font_obj=f_head)

    y += line_h
    seg2 = [("옵시디언 + ", BLACK), ("AI", TERRA)]
    draw_segments(draw, seg2, y, font_obj=f_head)

    y += line_h
    seg3 = [("npm 1줄 = 증식", BLACK)]
    draw_segments(draw, seg3, y, font_obj=f_head)

    f_sub = font(38, bold=False)
    draw_text_centered(draw, "토요일 = Claude Code", 680, f_sub, TERRA)

    draw_sparkle_4point(draw, 110, 870, 28, fill=TERRA, w_main=8, w_diag=4)
    draw_footer(draw, 1)
    img.save(OUT_DIR / "2026-05-04_vol009_ko_01_cover.png", "PNG")
    print("OK: ko_01_cover")


def slide_ko_2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "WHY · 왜 Claude Code 이 필수인가", "MON", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "INSTALL + RUN", font=f_kicker, fill=BLACK)

    f_title = font(72, bold=True)
    draw_text_centered(draw, "지식이 흩어지면", 180, f_title, BLACK)
    seg = [("기억 ", BLACK), ("0", TERRA), (" → 검색 ", BLACK), ("∞", TERRA)]
    draw_segments(draw, seg, 270, font_obj=f_title)

    f_subtitle = font(28, bold=False)
    draw_text_centered(draw, "npm 1줄 = AI 코드 도우미 증식", 380, f_subtitle, GRAY)

    items = [
        ("NPM", "npm install -g claude-code", PURPLE),
        ("API KEY", "ANTHROPIC_API_KEY 등록", PINK),
        ("INIT", "프로젝트 폴더 /init", AMBER),
        ("PROMPT", "자연어 프롬프트", GREEN),
    ]

    y0 = 460
    card_h = 110
    gap = 14
    for i, (label, role, color) in enumerate(items):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_name = font(34, bold=True)
        draw.text((100, y + 18), label, font=f_name, fill=BLACK)
        f_role = font(26, bold=False)
        draw.text((100, y + 64), role, font=f_role, fill=GRAY)

    draw_footer(draw, 2)
    img.save(OUT_DIR / "2026-05-04_vol009_ko_02_why.png", "PNG")
    print("OK: ko_02_why")


def slide_ko_3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "HOW · 3 STEPS · 5분", "MON", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "HANDS-ON", font=f_kicker, fill=BLACK)

    f_title = font(80, bold=True)
    seg = [("3", TERRA), (" STEPS = ", BLACK), ("5", TERRA), ("분", BLACK)]
    draw_segments(draw, seg, 180, font_obj=f_title)

    f_sub = font(30, bold=False)
    draw_text_centered(draw, "캡처 → 정리 → AI 검색", 290, f_sub, GRAY)

    steps = [
        ("STEP 1", "캡처 (1분)", "npm install -g claude-code", PURPLE),
        ("STEP 2", "정리 (3분)", "API 키 + /init 실행", PINK),
        ("STEP 3", "AI 검색 (1분)", "자연어 프롬프트", GREEN),
    ]

    y0 = 400
    card_h = 160
    gap = 24
    for i, (step, title, code, color) in enumerate(steps):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_step = font(22, bold=True)
        draw.text((100, y + 22), step, font=f_step, fill=color)
        f_t = font(32, bold=True)
        draw.text((100, y + 56), title, font=f_t, fill=BLACK)
        f_c = font(22, bold=False)
        draw.text((100, y + 110), code, font=f_c, fill=GRAY)

    draw_footer(draw, 3)
    img.save(OUT_DIR / "2026-05-04_vol009_ko_03_how.png", "PNG")
    print("OK: ko_03_how")


def slide_ko_4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_kicker = font(22, bold=True)
    draw.text((60, 80), "FOLLOW THE JOURNEY", font=f_kicker, fill=BLACK)
    draw_sparkle_4point(draw, W - 100, 95, 22, fill=TERRA, w_main=6, w_diag=3)

    f_head = font(72, bold=True)
    draw_text_centered(draw, "댓글 'DREAMTEAM'", 200, f_head, BLACK)
    seg = [("VOL.009", TERRA), (" 라이브러리 발송", BLACK)]
    draw_segments(draw, seg, 295, font_obj=f_head)

    f_day_label = font(36, bold=True)
    f_day_content = font(36, bold=True)
    items = [
        ("MON 월", "Claude Code", False),
        ("TUE 화", "AI 트렌드", False),
        ("WED 수", "드림팀 스토리", False),
        ("THU 목", "튜토리얼", False),
        ("FRI 금", "MCP 리뷰", False),
        ("MON 토", "Claude Code", True),
    ]
    y = 440
    for label, content, today in items:
        draw.text((180, y), label, font=f_day_label, fill=TERRA)
        color = TERRA if today else BLACK
        draw.text((430, y), "—  " + content, font=f_day_content, fill=color)
        y += 50

    box_x, box_y = 60, 800
    box_w_, box_h_ = W - 120, 130
    draw.rounded_rectangle([box_x, box_y, box_x + box_w_, box_y + box_h_], radius=16, fill=TERRA)
    f_cta = font(30, bold=True)
    f_cta2 = font(26, bold=True)
    draw_text_centered(draw, "매일 다른 VOL · 매일 새로운 가치", 822, f_cta, WHITE)
    draw_text_centered(draw, "오늘은 D+12 Claude Code Claude Code 설치 가이드", 868, f_cta2, WHITE)
    draw_sparkle_4point(draw, W - 130, 865, 14, fill=WHITE, w_main=4, w_diag=2)

    f_note = font(20, bold=False)
    draw.text((60, 960), "댓글 + DM 답글 모두 자동 (24h 내)", font=f_note, fill=GRAY)

    f_page = font(22, bold=True)
    text = "4/4 · @bella_ai_auto"
    tw, _ = text_size(draw, text, f_page)
    draw.text((W - 60 - tw, 960), text, font=f_page, fill=GRAY)

    img.save(OUT_DIR / "2026-05-04_vol009_ko_04_cta.png", "PNG")
    print("OK: ko_04_cta")


# ==================== EN ====================

def slide_en_1():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "VOL.009 — 2026.05.02 · MONDAY", "D+12", sparkle=True)

    f_head = font(94, bold=True)
    line_h = 116
    y = 250

    seg1 = [("Your ", BLACK), ("Claude Code", TERRA)]
    draw_segments(draw, seg1, y, font_obj=f_head)

    y += line_h
    seg2 = [("Obsidian + ", BLACK), ("AI", TERRA)]
    draw_segments(draw, seg2, y, font_obj=f_head)

    y += line_h
    seg3 = [("365-day Knowledge System", BLACK)]
    draw_segments(draw, seg3, y, font_obj=f_head)

    f_sub = font(40, bold=False, italic=True, en=True)
    draw_text_centered(draw, "Monday — Claude Code", 680, f_sub, TERRA)

    draw_sparkle_4point(draw, 110, 870, 28, fill=TERRA, w_main=8, w_diag=4)
    draw_footer(draw, 1)
    img.save(OUT_DIR / "2026-05-04_vol009_en_01_cover.png", "PNG")
    print("OK: en_01_cover")


def slide_en_2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "WHY · The Claude Code Power", "MON", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "INSTALL + RUN", font=f_kicker, fill=BLACK)

    f_title = font(72, bold=True)
    draw_text_centered(draw, "Scattered knowledge =", 180, f_title, BLACK)
    seg = [("Memory ", BLACK), ("0", TERRA), (" -> Search ", BLACK), ("Inf", TERRA)]
    draw_segments(draw, seg, 270, font_obj=f_title)

    f_subtitle = font(28, bold=False)
    draw_text_centered(draw, "npm 1 line = AI coding instantly", 380, f_subtitle, GRAY)

    items = [
        ("NPM", "npm install -g claude-code", PURPLE),
        ("API KEY", "ANTHROPIC_API_KEY", PINK),
        ("INIT", "/init in your repo", AMBER),
        ("PROMPT", "ask anything natural language", GREEN),
    ]

    y0 = 460
    card_h = 110
    gap = 14
    for i, (label, role, color) in enumerate(items):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_name = font(34, bold=True)
        draw.text((100, y + 18), label, font=f_name, fill=BLACK)
        f_role = font(26, bold=False)
        draw.text((100, y + 64), role, font=f_role, fill=GRAY)

    draw_footer(draw, 2)
    img.save(OUT_DIR / "2026-05-04_vol009_en_02_why.png", "PNG")
    print("OK: en_02_why")


def slide_en_3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "HOW · 3 STEPS · 5 min", "MON", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "HANDS-ON", font=f_kicker, fill=BLACK)

    f_title = font(80, bold=True)
    seg = [("3", TERRA), (" STEPS = ", BLACK), ("5", TERRA), (" min", BLACK)]
    draw_segments(draw, seg, 180, font_obj=f_title)

    f_sub = font(30, bold=False)
    draw_text_centered(draw, "Install -> API Key -> Run", 290, f_sub, GRAY)

    steps = [
        ("STEP 1", "Install (1m)", "npm install -g claude-code", PURPLE),
        ("STEP 2", "API Key (3m)", "set ANTHROPIC_API_KEY env", PINK),
        ("STEP 3", "Run (1m)", "/init then ask in plain English", GREEN),
    ]

    y0 = 400
    card_h = 160
    gap = 24
    for i, (step, title, code, color) in enumerate(steps):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_step = font(22, bold=True)
        draw.text((100, y + 22), step, font=f_step, fill=color)
        f_t = font(32, bold=True)
        draw.text((100, y + 56), title, font=f_t, fill=BLACK)
        f_c = font(22, bold=False)
        draw.text((100, y + 110), code, font=f_c, fill=GRAY)

    draw_footer(draw, 3)
    img.save(OUT_DIR / "2026-05-04_vol009_en_03_how.png", "PNG")
    print("OK: en_03_how")


def slide_en_4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_kicker = font(22, bold=True)
    draw.text((60, 80), "FOLLOW THE JOURNEY", font=f_kicker, fill=BLACK)
    draw_sparkle_4point(draw, W - 100, 95, 22, fill=TERRA, w_main=6, w_diag=3)

    f_head = font(76, bold=True)
    draw_text_centered(draw, "Comment 'DREAMTEAM'", 200, f_head, BLACK)
    seg = [("Get ", BLACK), ("VOL.009", TERRA), (" library via DM", BLACK)]
    draw_segments(draw, seg, 305, font_obj=f_head)

    f_day_label = font(36, bold=True)
    f_day_content = font(36, bold=True)
    items = [
        ("MON", "Claude Code", False),
        ("TUE", "AI Trends", False),
        ("WED", "Dream Team", False),
        ("THU", "Tutorial", False),
        ("FRI", "MCP Review", False),
        ("MON", "Claude Code", True),
    ]
    y = 440
    for label, content, today in items:
        draw.text((220, y), label, font=f_day_label, fill=TERRA)
        color = TERRA if today else BLACK
        draw.text((400, y), "—  " + content, font=f_day_content, fill=color)
        y += 50

    box_x, box_y = 60, 800
    box_w_, box_h_ = W - 120, 130
    draw.rounded_rectangle([box_x, box_y, box_x + box_w_, box_y + box_h_], radius=16, fill=TERRA)
    f_cta = font(30, bold=True)
    f_cta2 = font(26, bold=True)
    draw_text_centered(draw, "Different VOL - Fresh Value Daily", 822, f_cta, WHITE)
    draw_text_centered(draw, "Today: D+12 Claude Code Claude Code install", 868, f_cta2, WHITE)
    draw_sparkle_4point(draw, W - 130, 865, 14, fill=WHITE, w_main=4, w_diag=2)

    f_note = font(20, bold=False, italic=True, en=True)
    draw.text((60, 960), "Public reply + DM auto (within 24h)", font=f_note, fill=GRAY)

    f_page = font(22, bold=True)
    text = "4/4 · @bella_ai_auto"
    tw, _ = text_size(draw, text, f_page)
    draw.text((W - 60 - tw, 960), text, font=f_page, fill=GRAY)

    img.save(OUT_DIR / "2026-05-04_vol009_en_04_cta.png", "PNG")
    print("OK: en_04_cta")


if __name__ == "__main__":
    print("=" * 50)
    print("VOL.009 D+5 Tone — Claude Code 5분 설치")
    print("=" * 50)
    slide_ko_1()
    slide_ko_2()
    slide_ko_3()
    slide_ko_4()
    slide_en_1()
    slide_en_2()
    slide_en_3()
    slide_en_4()
    print("=" * 50)
    print(f"Done. Output: {OUT_DIR}")

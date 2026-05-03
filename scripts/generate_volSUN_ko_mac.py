"""
VOL.SUN — 2026.05.03 · SUNDAY 주간회고 (KO) — Mac mini
주제: 이번 주 우리 드림팀이 얻은 것 — D+8~D+11 4일 압축 회고
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path.home() / "bella-ai-intel/public_assets/instagram/2026-05-03"
OUT_DIR.mkdir(parents=True, exist_ok=True)

APPLE_GOTHIC = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
ITALIC_EN = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"

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
        return ImageFont.truetype(ITALIC_EN, size)
    return ImageFont.truetype(APPLE_GOTHIC, size, index=6 if bold else 0)


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
    draw_meta_top(draw, "VOL.SUN — 2026.05.03 · SUNDAY", "D+11", sparkle=True)

    f_head = font(86, bold=True)
    line_h = 110

    y = 250
    seg1 = [("이번 주 ", BLACK), ("드림팀", TERRA)]
    draw_segments(draw, seg1, y, font_obj=f_head)

    y += line_h
    seg2 = [("이 얻은 것", BLACK)]
    draw_segments(draw, seg2, y, font_obj=f_head)

    y += line_h
    seg3 = [("D+8 → D+11 ", BLACK), ("4일 압축", TERRA)]
    draw_segments(draw, seg3, y, font_obj=f_head)

    f_sub = font(38, bold=False)
    draw_text_centered(draw, "일요일 = 회고", 680, f_sub, TERRA)

    draw_sparkle_4point(draw, 110, 870, 28, fill=TERRA, w_main=8, w_diag=4)
    draw_footer(draw, 1)
    img.save(OUT_DIR / "2026-05-03_volSUN_ko_01_cover.png", "PNG")
    print("OK: SUN_ko_01_cover")


def slide_ko_2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "WHY · 왜 일요일에 회고?", "SUN", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "WEEKLY RETROSPECTIVE", font=f_kicker, fill=BLACK)

    f_title = font(72, bold=True)
    draw_text_centered(draw, "지난 주 정리 =", 180, f_title, BLACK)
    seg = [("다음 주 시작 ", BLACK), ("3배", TERRA), (" 빠름", BLACK)]
    draw_segments(draw, seg, 270, font_obj=f_title)

    f_subtitle = font(28, bold=False)
    draw_text_centered(draw, "월요일 0시에 시작하는 게 아니라 일요일 21시부터", 380, f_subtitle, GRAY)

    items = [
        ("CLARITY", "흩어진 학습이 하나로", PURPLE),
        ("MOMENTUM", "다음 주 1순위가 명확", PINK),
        ("CADENCE", "주간 리듬이 손에 잡힘", AMBER),
        ("COMPOUND", "52주 = 1년치 자산", GREEN),
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
    img.save(OUT_DIR / "2026-05-03_volSUN_ko_02_why.png", "PNG")
    print("OK: SUN_ko_02_why")


def slide_ko_3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "HOW · 3 STEP 회고 · 10분", "SUN", sparkle=False)

    f_kicker = font(22, bold=True)
    draw.text((60, 120), "RETROSPECTIVE METHOD", font=f_kicker, fill=BLACK)

    f_title = font(80, bold=True)
    seg = [("3", TERRA), (" STEP = ", BLACK), ("10", TERRA), ("분", BLACK)]
    draw_segments(draw, seg, 180, font_obj=f_title)

    f_sub = font(30, bold=False)
    draw_text_centered(draw, "배움 → 막힘 → 다음 주 1가지", 290, f_sub, GRAY)

    steps = [
        ("STEP 1", "무엇을 배웠나 (3분)", "이번 주 핵심 학습 3개", PURPLE),
        ("STEP 2", "무엇이 막혔나 (3분)", "병목·미해결·실패한 것", PINK),
        ("STEP 3", "다음 주 1가지 (4분)", "딱 1개의 P0 결정", GREEN),
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
    img.save(OUT_DIR / "2026-05-03_volSUN_ko_03_how.png", "PNG")
    print("OK: SUN_ko_03_how")


def slide_ko_4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_kicker = font(22, bold=True)
    draw.text((60, 80), "FOLLOW THE JOURNEY", font=f_kicker, fill=BLACK)
    draw_sparkle_4point(draw, W - 100, 95, 22, fill=TERRA, w_main=6, w_diag=3)

    f_head = font(72, bold=True)
    draw_text_centered(draw, "댓글 'DREAMTEAM'", 200, f_head, BLACK)
    seg = [("주간회고 템플릿", TERRA), (" DM 발송", BLACK)]
    draw_segments(draw, seg, 295, font_obj=f_head)

    f_day_label = font(36, bold=True)
    f_day_content = font(36, bold=True)
    items = [
        ("MON 월", "Claude Code", False),
        ("TUE 화", "AI 트렌드", False),
        ("WED 수", "드림팀 스토리", False),
        ("THU 목", "튜토리얼", False),
        ("FRI 금", "MCP 리뷰", False),
        ("SAT 토", "SecondBrain", False),
        ("SUN 일", "주간회고", True),
    ]
    y = 410
    for label, content, today in items:
        draw.text((180, y), label, font=f_day_label, fill=TERRA)
        color = TERRA if today else BLACK
        draw.text((430, y), "—  " + content, font=f_day_content, fill=color)
        y += 48

    box_x, box_y = 60, 800
    box_w_, box_h_ = W - 120, 130
    draw.rounded_rectangle([box_x, box_y, box_x + box_w_, box_y + box_h_], radius=16, fill=TERRA)
    f_cta = font(30, bold=True)
    f_cta2 = font(26, bold=True)
    draw_text_centered(draw, "매일 다른 VOL · 매주 일요일 회고", 822, f_cta, WHITE)
    draw_text_centered(draw, "오늘은 D+11 · 4일 압축 주간회고", 868, f_cta2, WHITE)
    draw_sparkle_4point(draw, W - 130, 865, 14, fill=WHITE, w_main=4, w_diag=2)

    f_note = font(20, bold=False)
    draw.text((60, 960), "댓글 + DM 답글 모두 자동 (24h 내)", font=f_note, fill=GRAY)

    f_page = font(22, bold=True)
    text = "4/4 · @bella_ai_auto"
    tw, _ = text_size(draw, text, f_page)
    draw.text((W - 60 - tw, 960), text, font=f_page, fill=GRAY)

    img.save(OUT_DIR / "2026-05-03_volSUN_ko_04_cta.png", "PNG")
    print("OK: SUN_ko_04_cta")


if __name__ == "__main__":
    print("=" * 50)
    print("VOL.SUN — 2026.05.03 · SUNDAY 주간회고 (KO) Mac mini")
    print("=" * 50)
    slide_ko_1()
    slide_ko_2()
    slide_ko_3()
    slide_ko_4()
    print("=" * 50)
    print(f"Done. Output: {OUT_DIR}")

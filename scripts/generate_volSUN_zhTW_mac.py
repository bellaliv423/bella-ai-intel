"""
VOL.SUN — 2026.05.03 · SUNDAY 週回顧 (ZH 簡體中文) — Mac mini
주제: 這週夢之隊收穫了什麼 — D+8~D+11 4天濃縮回顧
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path.home() / "bella-ai-intel/public_assets/instagram/2026-05-03"
OUT_DIR.mkdir(parents=True, exist_ok=True)

APPLE_GOTHIC = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
HEITI_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
HEITI_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
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


def font_zh(size, bold=True):
    path = HEITI_MEDIUM if bold else HEITI_LIGHT
    return ImageFont.truetype(path, size, index=1)


def font_latin(size, bold=True):
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


def draw_meta_top(draw, left_text, right_badge_text, sparkle=True, y=70, latin_left=False):
    f = font_latin(24, bold=True) if latin_left else font_zh(24, bold=True)
    draw.text((60, y + 10), left_text, font=f, fill=BLACK)
    if right_badge_text:
        f_b = font_latin(22, bold=True)
        tw, th = text_size(draw, right_badge_text, f_b)
        spark_w = 30 if sparkle else 0
        badge_w = tw + 56 + spark_w
        bx = W - 60 - badge_w
        draw_pill_badge(draw, right_badge_text, bx, y, f_b, sparkle=sparkle)


def draw_footer(draw, page_num):
    draw.line([(60, H - 70), (W - 60, H - 70)], fill=GRAY_LIGHT, width=1)
    f = font_latin(22, bold=True)
    text = f"{page_num}/4 · @bella_ai_auto"
    tw, th = text_size(draw, text, f)
    draw.text((W - 60 - tw, H - 50), text, font=f, fill=GRAY)


# ==================== ZH (簡體中文) ====================

def slide_zh_1():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "VOL.SUN — 2026.05.03 · SUNDAY", "D+11", sparkle=True, latin_left=True)

    f_head = font_zh(86, bold=True)
    line_h = 110

    y = 250
    seg1 = [("這週", BLACK), ("夢之隊", TERRA)]
    draw_segments(draw, seg1, y, font_obj=f_head)

    y += line_h
    seg2 = [("收穫了什麼", BLACK)]
    draw_segments(draw, seg2, y, font_obj=f_head)

    y += line_h
    seg3 = [("D+8 → D+11 ", BLACK), ("4天濃縮", TERRA)]
    draw_segments(draw, seg3, y, font_obj=f_head)

    f_sub = font_zh(38, bold=False)
    draw_text_centered(draw, "週日 = 回顧", 680, f_sub, TERRA)

    draw_sparkle_4point(draw, 110, 870, 28, fill=TERRA, w_main=8, w_diag=4)
    draw_footer(draw, 1)
    img.save(OUT_DIR / "2026-05-03_volSUN_zh_01_cover.png", "PNG")
    print("OK: SUN_zh_01_cover")


def slide_zh_2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "WHY · 為什麼週日要回顧?", "SUN", sparkle=False, latin_left=False)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 120), "WEEKLY RETROSPECTIVE", font=f_kicker, fill=BLACK)

    f_title = font_zh(72, bold=True)
    draw_text_centered(draw, "整理上週 =", 180, f_title, BLACK)
    seg = [("下週啟動", BLACK), ("快3倍", TERRA)]
    draw_segments(draw, seg, 270, font_obj=f_title)

    f_subtitle = font_zh(28, bold=False)
    draw_text_centered(draw, "不是週一零點開始,而是週日21點起步", 380, f_subtitle, GRAY)

    items = [
        ("CLARITY", "零散學習匯成一線", PURPLE),
        ("MOMENTUM", "下週首要任務清晰", PINK),
        ("CADENCE", "每週節奏掌握在手", AMBER),
        ("COMPOUND", "52周 = 1年的資產", GREEN),
    ]

    y0 = 460
    card_h = 110
    gap = 14
    for i, (label, role, color) in enumerate(items):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_name = font_latin(34, bold=True)
        draw.text((100, y + 18), label, font=f_name, fill=BLACK)
        f_role = font_zh(26, bold=False)
        draw.text((100, y + 64), role, font=f_role, fill=GRAY)

    draw_footer(draw, 2)
    img.save(OUT_DIR / "2026-05-03_volSUN_zh_02_why.png", "PNG")
    print("OK: SUN_zh_02_why")


def slide_zh_3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "HOW · 3 STEP 回顧 · 10分鐘", "SUN", sparkle=False, latin_left=False)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 120), "RETROSPECTIVE METHOD", font=f_kicker, fill=BLACK)

    f_title = font_zh(80, bold=True)
    seg = [("3", TERRA), (" STEP = ", BLACK), ("10", TERRA), (" 分鐘", BLACK)]
    draw_segments(draw, seg, 180, font_obj=f_title)

    f_sub = font_zh(30, bold=False)
    draw_text_centered(draw, "學到 → 卡住 → 下週一件事", 290, f_sub, GRAY)

    steps = [
        ("STEP 1", "學到了什麼 (3分鐘)", "本週3個核心學習", PURPLE),
        ("STEP 2", "卡在哪裡 (3分鐘)", "瓶頸·未解決·失敗點", PINK),
        ("STEP 3", "下週一件事 (4分鐘)", "只定1個 P0 決定", GREEN),
    ]

    y0 = 400
    card_h = 160
    gap = 24
    for i, (step, title, code, color) in enumerate(steps):
        y = y0 + i * (card_h + gap)
        draw.rounded_rectangle([60, y, W - 60, y + card_h], radius=16, outline=BLACK, width=2)
        draw.rounded_rectangle([60, y, 72, y + card_h], radius=6, fill=color)

        f_step = font_latin(22, bold=True)
        draw.text((100, y + 22), step, font=f_step, fill=color)
        f_t = font_zh(32, bold=True)
        draw.text((100, y + 56), title, font=f_t, fill=BLACK)
        f_c = font_zh(22, bold=False)
        draw.text((100, y + 110), code, font=f_c, fill=GRAY)

    draw_footer(draw, 3)
    img.save(OUT_DIR / "2026-05-03_volSUN_zh_03_how.png", "PNG")
    print("OK: SUN_zh_03_how")


def slide_zh_4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 80), "FOLLOW THE JOURNEY", font=f_kicker, fill=BLACK)
    draw_sparkle_4point(draw, W - 100, 95, 22, fill=TERRA, w_main=6, w_diag=3)

    f_head = font_zh(72, bold=True)
    draw_text_centered(draw, "評論 'DREAMTEAM'", 200, f_head, BLACK)
    seg = [("週回顧模板", TERRA), (" DM 傳送", BLACK)]
    draw_segments(draw, seg, 295, font_obj=f_head)

    f_day_label = font_zh(36, bold=True)
    f_day_content = font_zh(36, bold=True)
    items = [
        ("MON 週一", "Claude Code", False),
        ("TUE 週二", "AI 趨勢", False),
        ("WED 週三", "夢之隊故事", False),
        ("THU 週四", "教程", False),
        ("FRI 週五", "MCP 評測", False),
        ("SAT 週六", "SecondBrain", False),
        ("SUN 週日", "週回顧", True),
    ]
    y = 410
    for label, content, today in items:
        draw.text((180, y), label, font=f_day_label, fill=TERRA)
        color = TERRA if today else BLACK
        draw.text((460, y), "—  " + content, font=f_day_content, fill=color)
        y += 48

    box_x, box_y = 60, 800
    box_w_, box_h_ = W - 120, 130
    draw.rounded_rectangle([box_x, box_y, box_x + box_w_, box_y + box_h_], radius=16, fill=TERRA)
    f_cta = font_zh(30, bold=True)
    f_cta2 = font_zh(26, bold=True)
    draw_text_centered(draw, "每日不同 VOL · 每週日回顧", 822, f_cta, WHITE)
    draw_text_centered(draw, "今日 D+11 · 4天濃縮週回顧", 868, f_cta2, WHITE)
    draw_sparkle_4point(draw, W - 130, 865, 14, fill=WHITE, w_main=4, w_diag=2)

    f_note = font_zh(20, bold=False)
    draw.text((60, 960), "評論 + DM 自動回覆 (24小時內)", font=f_note, fill=GRAY)

    f_page = font_latin(22, bold=True)
    text = "4/4 · @bella_ai_auto"
    tw, _ = text_size(draw, text, f_page)
    draw.text((W - 60 - tw, 960), text, font=f_page, fill=GRAY)

    img.save(OUT_DIR / "2026-05-03_volSUN_zh_04_cta.png", "PNG")
    print("OK: SUN_zh_04_cta")


if __name__ == "__main__":
    print("=" * 50)
    print("VOL.SUN — 2026.05.03 · SUNDAY 週回顧 (ZH 簡體中文) Mac mini")
    print("=" * 50)
    slide_zh_1()
    slide_zh_2()
    slide_zh_3()
    slide_zh_4()
    print("=" * 50)
    print(f"Done. Output: {OUT_DIR}")

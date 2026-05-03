"""
VOL.008 D+10 vol001 톤 — 4 ZH (简体中文) — Mac mini 版本
주제: SecondBrain 옵시디언 + Claude Code 지식관리
Translated from generate_vol008_v3_d5.py KO content to Simplified Chinese.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path.home() / "bella-ai-intel/public_assets/instagram/2026-05-02"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Mac fonts
APPLE_GOTHIC = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # 0=Regular, 6=Bold
HEITI_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"      # 1 = Heiti SC Light
HEITI_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"    # 1 = Heiti SC Medium
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
    """Simplified Chinese font — Heiti SC."""
    path = HEITI_MEDIUM if bold else HEITI_LIGHT
    return ImageFont.truetype(path, size, index=1)


def font_latin(size, bold=True):
    """Latin/numerics — AppleSDGothicNeo handles latin OK."""
    return ImageFont.truetype(APPLE_GOTHIC, size, index=6 if bold else 0)


def font(size, bold=True, italic=False, en=False):
    """Universal font fn used by helpers — defaults to ZH."""
    if italic and en:
        return ImageFont.truetype(ITALIC_EN, size)
    if en:
        return ImageFont.truetype(APPLE_GOTHIC, size, index=6 if bold else 0)
    return font_zh(size, bold=bold)


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


# ==================== ZH (简体中文) ====================

def slide_zh_1():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # left text uses latin font (numerics+SATURDAY)
    draw_meta_top(draw, "VOL.008 — 2026.05.02 · SATURDAY", "D+10", sparkle=True, latin_left=True)

    f_head = font_zh(94, bold=True)
    line_h = 116

    y = 250
    seg1 = [("我的", BLACK), ("第二大脑", TERRA)]
    draw_segments(draw, seg1, y, font_obj=f_head)

    y += line_h
    seg2 = [("Obsidian + ", BLACK), ("AI", TERRA)]
    # Use mixed font: render entire line with ZH font (Heiti SC handles latin too)
    draw_segments(draw, seg2, y, font_obj=f_head)

    y += line_h
    seg3 = [("365天累积系统", BLACK)]
    draw_segments(draw, seg3, y, font_obj=f_head)

    f_sub = font_zh(38, bold=False)
    draw_text_centered(draw, "周六 = SecondBrain", 680, f_sub, TERRA)

    draw_sparkle_4point(draw, 110, 870, 28, fill=TERRA, w_main=8, w_diag=4)
    draw_footer(draw, 1)
    img.save(OUT_DIR / "2026-05-02_vol008_zh_01_cover.png", "PNG")
    print("OK: zh_01_cover")


def slide_zh_2():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "WHY · 为什么必须有第二大脑", "SAT", sparkle=False, latin_left=False)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 120), "PARA + ZETTELKASTEN", font=f_kicker, fill=BLACK)

    f_title = font_zh(72, bold=True)
    draw_text_centered(draw, "知识一旦零散", 180, f_title, BLACK)
    seg = [("记忆 ", BLACK), ("0", TERRA), (" → 检索 ", BLACK), ("∞", TERRA)]
    draw_segments(draw, seg, 270, font_obj=f_title)

    f_subtitle = font_zh(28, bold=False)
    draw_text_centered(draw, "1 笔记 + 1 链接 = 365天后秒级检索", 380, f_subtitle, GRAY)

    items = [
        ("PROJECTS", "正在进行的工作", PURPLE),
        ("AREAS", "持续负责领域", PINK),
        ("RESOURCES", "参考资料", AMBER),
        ("ARCHIVE", "已完成存档", GREEN),
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
    img.save(OUT_DIR / "2026-05-02_vol008_zh_02_why.png", "PNG")
    print("OK: zh_02_why")


def slide_zh_3():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_meta_top(draw, "HOW · 3 STEPS · 5 分钟", "SAT", sparkle=False, latin_left=False)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 120), "HANDS-ON", font=f_kicker, fill=BLACK)

    f_title = font_zh(80, bold=True)
    seg = [("3", TERRA), (" STEPS = ", BLACK), ("5", TERRA), (" 分钟", BLACK)]
    draw_segments(draw, seg, 180, font_obj=f_title)

    f_sub = font_zh(30, bold=False)
    draw_text_centered(draw, "捕捉 → 整理 → AI 检索", 290, f_sub, GRAY)

    steps = [
        ("STEP 1", "捕捉 (1分钟)", "先丢进 Daily Note", PURPLE),
        ("STEP 2", "整理 (3分钟)", "PARA 文件夹 + 标签 + 双链", PINK),
        ("STEP 3", "AI 检索 (1分钟)", "用 Claude Code 即时召回", GREEN),
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
    img.save(OUT_DIR / "2026-05-02_vol008_zh_03_how.png", "PNG")
    print("OK: zh_03_how")


def slide_zh_4():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_kicker = font_latin(22, bold=True)
    draw.text((60, 80), "FOLLOW THE JOURNEY", font=f_kicker, fill=BLACK)
    draw_sparkle_4point(draw, W - 100, 95, 22, fill=TERRA, w_main=6, w_diag=3)

    f_head = font_zh(72, bold=True)
    draw_text_centered(draw, "评论 'DREAMTEAM'", 200, f_head, BLACK)
    seg = [("VOL.008", TERRA), (" 资料库自动发送", BLACK)]
    draw_segments(draw, seg, 295, font_obj=f_head)

    f_day_label = font_zh(36, bold=True)
    f_day_content = font_zh(36, bold=True)
    items = [
        ("MON 周一", "Claude Code", False),
        ("TUE 周二", "AI 趋势", False),
        ("WED 周三", "梦之队故事", False),
        ("THU 周四", "教程", False),
        ("FRI 周五", "MCP 评测", False),
        ("SAT 周六", "SecondBrain", True),
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
    f_cta = font_zh(30, bold=True)
    f_cta2 = font_zh(26, bold=True)
    draw_text_centered(draw, "每日不同 VOL · 每日新价值", 822, f_cta, WHITE)
    draw_text_centered(draw, "今日 D+10 SecondBrain PARA 系统", 868, f_cta2, WHITE)
    draw_sparkle_4point(draw, W - 130, 865, 14, fill=WHITE, w_main=4, w_diag=2)

    f_note = font_zh(20, bold=False)
    draw.text((60, 960), "评论 + DM 自动回复 (24小时内)", font=f_note, fill=GRAY)

    f_page = font_latin(22, bold=True)
    text = "4/4 · @bella_ai_auto"
    tw, _ = text_size(draw, text, f_page)
    draw.text((W - 60 - tw, 960), text, font=f_page, fill=GRAY)

    img.save(OUT_DIR / "2026-05-02_vol008_zh_04_cta.png", "PNG")
    print("OK: zh_04_cta")


if __name__ == "__main__":
    print("=" * 50)
    print("VOL.008 D+10 — SecondBrain (ZH 简体中文) Mac mini")
    print("=" * 50)
    slide_zh_1()
    slide_zh_2()
    slide_zh_3()
    slide_zh_4()
    print("=" * 50)
    print(f"Done. Output: {OUT_DIR}")

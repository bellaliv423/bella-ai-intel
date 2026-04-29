"""
VOL.005 KO 4장 한국어 캐러셀 PIL 생성
- PIL Pretendard 대신 malgunbd.ttf 사용 (Windows 기본, 한국어 안전)
- 1080x1080
- vol001 톤 6 criterion 100% 준수
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("D:/bella-ai-intel/public_assets/instagram/2026-04-29")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# 색상 (vol001 톤)
CREAM = "#fef9f5"
PURPLE = "#9333ea"
PINK = "#ec4899"
YELLOW = "#fbbf24"
GREEN = "#10b981"
BLACK = "#0f172a"
GRAY = "#6b7280"
WHITE = "#ffffff"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def gradient_bg(w, h, c1, c2):
    """대각선 그라디언트 배경 생성"""
    img = Image.new("RGB", (w, h))
    px = img.load()
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            px[x, y] = (r, g, b)
    return img


def draw_text_centered(draw, text, y, font_obj, fill, w=1080):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, y), text, font=font_obj, fill=fill)


# ===== 슬라이드 1 (커버) =====
def slide_1():
    img = gradient_bg(1080, 1080, PURPLE, PINK)
    draw = ImageDraw.Draw(img)
    # 큰 D+7
    draw_text_centered(draw, "D+7.", 240, font(180), WHITE)
    # 메인 메시지
    draw_text_centered(draw, "비개발자가 만든", 470, font(80), WHITE)
    draw_text_centered(draw, "AI 드림팀", 580, font(110), WHITE)
    # 서브
    draw_text_centered(draw, "수요일 = 드림팀 케이스", 760, font(40, bold=False), WHITE)
    # 출처
    draw.text((830, 1020), "@bella_ai_auto", font=font(28, bold=False), fill=WHITE)
    img.save(OUT_DIR / "vol005_ko_1.png", "PNG")
    print("OK: vol005_ko_1.png")


# ===== 슬라이드 2 (도트 매트릭스) =====
def slide_2():
    img = Image.new("RGB", (1080, 1080), CREAM)
    draw = ImageDraw.Draw(img)
    # 헤드라인
    draw_text_centered(draw, "AI 페르소나 17명", 130, font(80), BLACK)
    # 도트 매트릭스 4행 x 5열
    dot_size = 90
    gap = 50
    total_w = 5 * dot_size + 4 * gap
    start_x = (1080 - total_w) // 2
    start_y = 320

    waves = [
        [PURPLE] * 5,                              # Wave 1: 5개 보라
        [PINK] * 5,                                # Wave 2: 5개 핑크
        [YELLOW] * 4 + [None],                     # Wave 3: 4개 옐로우 + 1개 빈
        [GREEN] * 3 + [None] * 2,                  # Wave 4: 3개 그린 + 2개 빈
    ]

    for row, wave in enumerate(waves):
        y = start_y + row * (dot_size + gap)
        for col, color in enumerate(wave):
            x = start_x + col * (dot_size + gap)
            if color:
                draw.ellipse([x, y, x + dot_size, y + dot_size], fill=color)
            else:
                draw.ellipse([x, y, x + dot_size, y + dot_size], outline=GRAY, width=4)

    # Wave 라벨 (좌측)
    labels = ["Wave 1", "Wave 2", "Wave 3", "Wave 4"]
    for i, lab in enumerate(labels):
        y = start_y + i * (dot_size + gap) + dot_size // 2 - 18
        draw.text((50, y), lab, font=font(32), fill=GRAY)

    # 캡션
    draw_text_centered(draw, "Wave 1 → 4, 7일간 누적", 920, font(36, bold=False), GRAY)
    # 출처
    draw.text((830, 1020), "@bella_ai_auto", font=font(28, bold=False), fill=GRAY)
    img.save(OUT_DIR / "vol005_ko_2.png", "PNG")
    print("OK: vol005_ko_2.png")


# ===== 슬라이드 3 (3 x 3 그리드) =====
def slide_3():
    img = Image.new("RGB", (1080, 1080), CREAM)
    draw = ImageDraw.Draw(img)
    # 헤드라인
    draw_text_centered(draw, "동기화 = 3 × 3", 110, font(80), BLACK)

    # 좌측 (채널) — 컬러 카드
    channels = [("DKM", PURPLE), ("Notion", PINK), ("Slack", YELLOW)]
    devices = [("윈도우 데스크탑", BLACK), ("이동식 노트북", BLACK), ("Mac mini 24/7", BLACK)]

    card_w, card_h = 360, 130
    gap_y = 40
    start_y = 280

    # 좌측 컬러 카드
    for i, (label, color) in enumerate(channels):
        x = 80
        y = start_y + i * (card_h + gap_y)
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=24, fill=color)
        bbox = draw.textbbox((0, 0), label, font=font(56))
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x + (card_w - tw) // 2, y + (card_h - th) // 2 - 8), label, font=font(56), fill=WHITE)

    # 우측 박스 (디바이스)
    for i, (label, color) in enumerate(devices):
        x = 1080 - 80 - card_w
        y = start_y + i * (card_h + gap_y)
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=24, outline=BLACK, width=4)
        bbox = draw.textbbox((0, 0), label, font=font(40))
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x + (card_w - tw) // 2, y + (card_h - th) // 2 - 8), label, font=font(40), fill=BLACK)

    # 가운데 점선 연결
    for i in range(3):
        y = start_y + i * (card_h + gap_y) + card_h // 2
        for x in range(450, 640, 18):
            draw.ellipse([x, y - 4, x + 8, y + 4], fill=GRAY)

    # 라벨
    draw.text((180, 220), "채널", font=font(36), fill=GRAY)
    draw.text((830, 220), "디바이스", font=font(36), fill=GRAY)

    # 출처
    draw.text((830, 1020), "@bella_ai_auto", font=font(28, bold=False), fill=GRAY)
    img.save(OUT_DIR / "vol005_ko_3.png", "PNG")
    print("OK: vol005_ko_3.png")


# ===== 슬라이드 4 (CTA) =====
def slide_4():
    img = gradient_bg(1080, 1080, PURPLE, PINK)
    draw = ImageDraw.Draw(img)

    # 흰 카드 오버레이
    card_x, card_y = 90, 180
    card_w, card_h = 900, 720
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=40,
        fill=WHITE
    )

    # 카드 안 헤드라인
    bbox = draw.textbbox((0, 0), "자료 받기", font=font(100))
    tw = bbox[2] - bbox[0]
    draw.text((card_x + (card_w - tw) // 2, card_y + 70), "자료 받기", font=font(100), fill=BLACK)

    # 별 모양 도형 (이모지 대신 PIL 그리기, vol001 톤 R09)
    star_x, star_y = card_x + card_w - 110, card_y + 80
    # 노란 동그라미 + 가운데 점 (별 대용 - 안전한 도형)
    draw.ellipse([star_x, star_y, star_x + 50, star_y + 50], fill=YELLOW)
    draw.ellipse([star_x + 18, star_y + 18, star_x + 32, star_y + 32], fill=WHITE)

    # 본문
    bbox = draw.textbbox((0, 0), "댓글 'DREAMTEAM' 남기면", font=font(40, bold=False))
    tw = bbox[2] - bbox[0]
    draw.text((card_x + (card_w - tw) // 2, card_y + 220), "댓글 'DREAMTEAM' 남기면", font=font(40, bold=False), fill=GRAY)
    bbox = draw.textbbox((0, 0), "DM으로 PDF 자동 발송", font=font(40, bold=False))
    tw = bbox[2] - bbox[0]
    draw.text((card_x + (card_w - tw) // 2, card_y + 280), "DM으로 PDF 자동 발송", font=font(40, bold=False), fill=GRAY)

    # 자격 3가지 — 체크박스를 초록 동그라미로 대체 (vol001 톤 R09)
    items = ["팔로우", "좋아요", "댓글"]
    for i, item in enumerate(items):
        y = card_y + 410 + i * 80
        # 초록 동그라미 (체크박스 대용)
        cx, cy = card_x + 260, y + 25
        r = 22
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
        # 가운데 흰색 작은 사각형 (체크 표시)
        draw.rectangle([cx - 10, cy - 4, cx + 10, cy + 4], fill=WHITE)
        # 텍스트
        draw.text((card_x + 320, y + 5), item, font=font(50), fill=BLACK)

    # 출처
    draw.text((780, 1020), "@bella_ai_auto · D+7", font=font(28, bold=False), fill=WHITE)
    img.save(OUT_DIR / "vol005_ko_4.png", "PNG")
    print("OK: vol005_ko_4.png")


if __name__ == "__main__":
    print("=" * 50)
    print("VOL.005 KO Korean carousel generation")
    print("=" * 50)
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    print("=" * 50)
    print("Done. Output: D:/bella-ai-intel/public_assets/instagram/2026-04-29/")

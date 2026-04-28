"""
KO 4장 캐러셀 PIL 합성 (Pretendard 폴백 맑은 고딕, 깨짐 0%)
1080x1080, Anthropic 브랜드 톤, 한국어 풀 컨텐츠
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

FONTS = "C:/Windows/Fonts"
F_BOLD = os.path.join(FONTS, "malgunbd.ttf")
F_REG = os.path.join(FONTS, "malgun.ttf")

CREAM = (240, 238, 230)
BROWN = (204, 120, 92)
BROWN_LIGHT = (255, 245, 236)
DARK = (25, 25, 25)
GRAY = (128, 112, 96)
WHITE = (255, 255, 255)


def add_star(draw, x, y, size=40, color=BROWN):
    """간단한 ✷ 별"""
    # 점 4개
    for dx, dy in [(0, -size//2), (0, size//2), (-size//2, 0), (size//2, 0)]:
        draw.line([(x, y), (x + dx, y + dy)], fill=color, width=3)


def slide_1(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 26)
    f_h1 = ImageFont.truetype(F_BOLD, 88)
    f_sub = ImageFont.truetype(F_REG, 32)
    f_handle = ImageFont.truetype(F_REG, 26)

    # 라벨 박스
    d.rounded_rectangle([(80, 70), (700, 130)], radius=10, fill=BROWN)
    d.text((100, 82), "VOL.003 — DREAMTEAM SERIES", fill=WHITE, font=f_label)

    # 메인 헤드라인
    d.text((80, 280), "Claude Skills", fill=DARK, font=f_h1)
    d.text((80, 400), "× MCP", fill=DARK, font=f_h1)
    d.text((80, 520), "이번 주 트렌드", fill=DARK, font=f_h1)

    # 부제
    d.text((80, 700), "비개발자 1인 + 3봇 = 20명 24/7 운영", fill=BROWN, font=f_sub)
    d.text((80, 750), "월~토 매주 6회 시리즈", fill=GRAY, font=f_sub)

    # 핸들 + 별
    d.text((80, 950), "@bella_ai_auto", fill=DARK, font=f_handle)
    add_star(d, 1010, 80, size=30, color=BROWN)

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_2(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 22)
    f_h2 = ImageFont.truetype(F_BOLD, 80)
    f_check = ImageFont.truetype(F_REG, 32)
    f_box = ImageFont.truetype(F_BOLD, 26)
    f_box_sm = ImageFont.truetype(F_REG, 22)

    # 라벨
    d.rounded_rectangle([(80, 70), (300, 125)], radius=8, fill=BROWN)
    d.text((100, 85), "01 / 트렌드", fill=WHITE, font=f_label)

    # 타이틀
    d.text((80, 220), "Claude Skills", fill=DARK, font=f_h2)

    # 체크리스트
    bullets = [
        "매번 프롬프트 안 써도 자동 호출",
        "폴더 구조만 만들면 끝",
        "비개발자도 5분 안에 첫 스킬 완성",
    ]
    y = 420
    for b in bullets:
        d.text((100, y), "✓", fill=BROWN, font=f_check)
        d.text((150, y), b, fill=DARK, font=f_check)
        y += 70

    # 하단 강조 박스 (Crail Brown)
    d.rounded_rectangle([(80, 820), (1000, 940)], radius=12, fill=BROWN)
    d.text((100, 840), "예시: 인스타 발행 / 회의록 / 업무일지 자동화", fill=WHITE, font=f_box)
    d.text((100, 885), "5분 셋업 → 매일 자동", fill=WHITE, font=f_box_sm)

    add_star(d, 1010, 1010, size=24, color=BROWN)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_3(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 22)
    f_h2 = ImageFont.truetype(F_BOLD, 64)
    f_card = ImageFont.truetype(F_BOLD, 26)
    f_card_sm = ImageFont.truetype(F_REG, 22)
    f_box = ImageFont.truetype(F_BOLD, 28)

    # 라벨
    d.rounded_rectangle([(80, 70), (300, 125)], radius=8, fill=BROWN)
    d.text((100, 85), "02 / 트렌드", fill=WHITE, font=f_label)

    # 타이틀
    d.text((80, 220), "MCP — Model", fill=DARK, font=f_h2)
    d.text((80, 300), "Context Protocol", fill=DARK, font=f_h2)

    # 3 카드 (햄스터즈 / 만능이 / 퍼피즈) — 이모지 대신 색상 원/도형
    cards = [
        ("HAMSTERZ", "햄스터즈", "윈도우 데스크탑", (217, 119, 87)),   # 주황
        ("MANNEUNGI", "만능이", "Slack 통합", (124, 58, 237)),         # 보라
        ("PUPPYZ", "퍼피즈", "맥미니 24/7", (236, 72, 153)),           # 핑크
    ]
    card_w = 290
    card_h = 220
    gap = 20
    start_x = (1080 - 3 * card_w - 2 * gap) // 2
    y = 480
    f_badge = ImageFont.truetype(F_BOLD, 16)
    for i, (badge, name, desc, color) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        d.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=12, fill=WHITE, outline=color, width=2)
        # 색상 원 도트
        d.ellipse([(x + 30, y + 30), (x + 70, y + 70)], fill=color)
        # 영문 라벨 (배지)
        d.text((x + 30, y + 90), badge, fill=color, font=f_badge)
        # 한국어 이름
        d.text((x + 30, y + 115), name, fill=DARK, font=f_card)
        # 디바이스
        d.text((x + 30, y + 165), desc, fill=GRAY, font=f_card_sm)

    # 하단 강조
    d.rounded_rectangle([(80, 800), (1000, 880)], radius=12, fill=BROWN_LIGHT, outline=BROWN, width=2)
    d.text((100, 820), "비개발자 1인 = 20명 마케팅 페르소나 24/7", fill=BROWN, font=f_box)

    add_star(d, 1010, 1010, size=24, color=BROWN)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_4_cta(out):
    """CTA — 가벼운 약속 (Phase 0~5 약속 제거)"""
    img = Image.new('RGB', (1080, 1080), BROWN)
    d = ImageDraw.Draw(img)

    f_h1 = ImageFont.truetype(F_BOLD, 70)
    f_handle = ImageFont.truetype(F_BOLD, 54)
    f_box = ImageFont.truetype(F_REG, 32)

    # 큰 헤드라인 (3줄)
    d.text((140, 230), "댓글 「DREAMTEAM」", fill=WHITE, font=f_h1)
    d.text((180, 340), "남기시면", fill=WHITE, font=f_h1)
    d.text((180, 450), "드림팀 자료", fill=WHITE, font=f_h1)

    # 가벼운 약속 박스 (가격 X, 풀 디테일 X)
    d.rounded_rectangle([(150, 600), (930, 800)], radius=12, outline=WHITE, width=3)
    d.text((180, 625), "  드림팀 한 장 소개", fill=WHITE, font=f_box)
    d.text((180, 680), "  매주 6일 시리즈 캘린더", fill=WHITE, font=f_box)
    d.text((180, 735), "  Claude Skills 가이드 PDF", fill=WHITE, font=f_box)
    # 체크표시 (직접 그림)
    for cy in [641, 696, 751]:
        d.line([(165, cy), (172, cy + 8)], fill=WHITE, width=3)
        d.line([(172, cy + 8), (182, cy - 5)], fill=WHITE, width=3)

    # 핸들
    d.text((280, 880), "@bella_ai_auto", fill=WHITE, font=f_handle)

    # 별
    add_star(d, 980, 80, size=36, color=WHITE)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


if __name__ == '__main__':
    out_dir = Path('D:/bella-ai-intel/public_assets/instagram')
    out_dir.mkdir(parents=True, exist_ok=True)

    slide_1(out_dir / 'vol003_ko_1.png')
    slide_2(out_dir / 'vol003_ko_2.png')
    slide_3(out_dir / 'vol003_ko_3.png')
    slide_4_cta(out_dir / 'vol003_ko_4.png')
    print('\n[DONE] 4 KO carousel slides (한국어 PIL 합성)')

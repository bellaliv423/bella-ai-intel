"""
KO 4장 캐러셀 PIL 합성 (Pretendard 한국어, ZH 영문 톤 디자인 그대로 적용)
1080x1080, 영문 nano banana 톤 (둥근 카드 + 색상 도트 + Crail Brown 강조)
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
ORANGE = (217, 119, 87)
PURPLE = (124, 58, 237)
PINK = (236, 72, 153)


def slide_1(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 28)
    f_h1 = ImageFont.truetype(F_BOLD, 92)
    f_sub = ImageFont.truetype(F_REG, 30)
    f_handle = ImageFont.truetype(F_BOLD, 32)
    f_plus = ImageFont.truetype(F_BOLD, 40)

    # 라벨 박스 (Crail Brown)
    d.rounded_rectangle([(80, 95), (740, 165)], radius=8, fill=BROWN)
    d.text((105, 113), "VOL.003 — DREAMTEAM SERIES", fill=WHITE, font=f_label)

    # 메인 헤드라인 (3줄)
    d.text((80, 270), "Claude Skills", fill=DARK, font=f_h1)
    d.text((80, 390), "× MCP", fill=DARK, font=f_h1)
    d.text((80, 510), "이번 주 트렌드", fill=DARK, font=f_h1)

    # 부제 2줄
    d.text((80, 690), "비개발자 1인 + 3봇 = 20명 24/7 운영", fill=DARK, font=f_sub)
    d.text((80, 740), "월~토 매주 6회 시리즈", fill=GRAY, font=f_sub)

    # 핸들 (하단 중앙)
    d.text((350, 940), "@bella_ai_auto", fill=DARK, font=f_handle)

    # + 표시 (우상단)
    d.text((970, 80), "+", fill=BROWN, font=f_plus)

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_2(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 26)
    f_h2 = ImageFont.truetype(F_BOLD, 100)
    f_check = ImageFont.truetype(F_BOLD, 36)
    f_box = ImageFont.truetype(F_BOLD, 28)
    f_plus = ImageFont.truetype(F_BOLD, 36)

    # 라벨
    d.rounded_rectangle([(80, 95), (290, 155)], radius=8, fill=BROWN)
    d.text((105, 110), "01 / 트렌드", fill=WHITE, font=f_label)

    # 타이틀
    d.text((80, 280), "Claude Skills", fill=DARK, font=f_h2)

    # 체크리스트 3개 (둥근 원형 체크)
    bullets = [
        "매번 프롬프트 안 써도 자동 호출",
        "폴더 구조만 만들면 끝",
        "5분 안에 첫 스킬 완성 (비개발자)",
    ]
    y = 530
    for b in bullets:
        # 원형 체크
        d.ellipse([(85, y - 5), (135, y + 45)], outline=BROWN, width=3)
        # 체크 표시
        d.line([(98, y + 22), (110, y + 32)], fill=BROWN, width=4)
        d.line([(110, y + 32), (125, y + 12)], fill=BROWN, width=4)
        # 텍스트
        d.text((160, y), b, fill=DARK, font=f_check)
        y += 75

    # 하단 강조 박스 (Crail Brown)
    d.rounded_rectangle([(80, 880), (1000, 980)], radius=10, fill=BROWN)
    d.text((100, 895), "예시: 인스타 발행 / 회의록 / 업무일지", fill=WHITE, font=f_box)
    d.text((100, 935), "자동 발행 — 5분 셋업, 매일 자동", fill=WHITE, font=f_box)

    # +
    d.text((970, 1010), "+", fill=BROWN, font=f_plus)

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_3(out):
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 26)
    f_h2 = ImageFont.truetype(F_BOLD, 76)
    f_card_name = ImageFont.truetype(F_BOLD, 22)
    f_card_kr = ImageFont.truetype(F_BOLD, 24)
    f_card_desc = ImageFont.truetype(F_REG, 18)
    f_box = ImageFont.truetype(F_BOLD, 26)
    f_plus = ImageFont.truetype(F_BOLD, 36)

    # 라벨
    d.rounded_rectangle([(80, 95), (290, 155)], radius=8, fill=BROWN)
    d.text((105, 110), "02 / 트렌드", fill=WHITE, font=f_label)

    # 타이틀 (3줄)
    d.text((80, 240), "MCP — Model", fill=DARK, font=f_h2)
    d.text((80, 320), "Context Protocol", fill=DARK, font=f_h2)

    # 3 카드 (영문 톤 그대로)
    cards = [
        ("HAMSTERZ", "햄스터즈", "윈도우 데스크탑", ORANGE),
        ("MANNEUNGI", "만능이", "Slack 통합", PURPLE),
        ("PUPPYZ", "퍼피즈", "맥미니 24/7", PINK),
    ]
    card_w = 300
    card_h = 200
    gap = 15
    start_x = (1080 - 3 * card_w - 2 * gap) // 2
    y = 560
    for i, (badge, name, desc, color) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        # 카드 박스
        d.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=14, fill=WHITE, outline=BROWN, width=2)
        # 색상 도트
        d.ellipse([(x + 25, y + 30), (x + 55, y + 60)], fill=color)
        # 영문 라벨
        d.text((x + 70, y + 35), badge, fill=color, font=f_card_name)
        # 한국어 이름
        d.text((x + 25, y + 90), name, fill=DARK, font=f_card_kr)
        # 디바이스
        d.text((x + 25, y + 135), desc, fill=GRAY, font=f_card_desc)

    # 하단 강조 박스 (light cream + Crail Brown 텍스트)
    d.rounded_rectangle([(80, 870), (1000, 950)], radius=10, fill=BROWN_LIGHT, outline=BROWN, width=2)
    d.text((100, 895), "비개발자 1인 = 20명 마케팅 페르소나 24/7", fill=BROWN, font=f_box)

    # +
    d.text((970, 1010), "+", fill=BROWN, font=f_plus)

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_4_cta(out):
    """CTA — 가벼운 약속 + 한국어"""
    img = Image.new('RGB', (1080, 1080), BROWN)
    d = ImageDraw.Draw(img)

    f_h1 = ImageFont.truetype(F_BOLD, 80)
    f_handle = ImageFont.truetype(F_BOLD, 60)
    f_box = ImageFont.truetype(F_BOLD, 34)

    # 큰 헤드라인 (3줄)
    d.text((130, 220), "댓글 「DREAMTEAM」", fill=WHITE, font=f_h1)
    d.text((180, 320), "남기시면", fill=WHITE, font=f_h1)
    d.text((180, 420), "드림팀 자료 받기", fill=WHITE, font=f_h1)

    # 약속 박스 (가벼운, 가격 X)
    d.rounded_rectangle([(120, 590), (960, 800)], radius=14, outline=WHITE, width=3)
    promises = [
        "드림팀 한 장 소개 PNG",
        "매주 6일 시리즈 캘린더",
        "Claude Skills 가이드 PDF",
    ]
    y = 615
    for p in promises:
        # 체크 표시 (직접 그림)
        d.line([(165, y + 25), (180, y + 40)], fill=WHITE, width=4)
        d.line([(180, y + 40), (200, y + 15)], fill=WHITE, width=4)
        d.text((230, y + 5), p, fill=WHITE, font=f_box)
        y += 65

    # 핸들
    d.text((290, 880), "@bella_ai_auto", fill=WHITE, font=f_handle)

    # ✦ 별 (직접)
    sx, sy = 980, 80
    d.line([(sx, sy - 25), (sx, sy + 25)], fill=WHITE, width=2)
    d.line([(sx - 25, sy), (sx + 25, sy)], fill=WHITE, width=2)
    d.line([(sx - 18, sy - 18), (sx + 18, sy + 18)], fill=WHITE, width=2)
    d.line([(sx - 18, sy + 18), (sx + 18, sy - 18)], fill=WHITE, width=2)

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


if __name__ == '__main__':
    out_dir = Path('D:/bella-ai-intel/public_assets/instagram')
    out_dir.mkdir(parents=True, exist_ok=True)

    slide_1(out_dir / 'vol003_ko_1.png')
    slide_2(out_dir / 'vol003_ko_2.png')
    slide_3(out_dir / 'vol003_ko_3.png')
    slide_4_cta(out_dir / 'vol003_ko_4.png')
    print('\n[DONE] 4 KO carousel slides (한국어 PIL Pretendard, ZH 톤 디자인)')

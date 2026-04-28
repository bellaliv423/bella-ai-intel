"""
VOL.003 KO 4장 — vol001 디자인 명세서 풀 적용 (PIL Pretendard)
영구 기준선: ~/.claude/skills/bellanest-content-funnel/design_reference/vol001_design_spec.md
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

FONTS = "C:/Windows/Fonts"
F_BOLD = os.path.join(FONTS, "malgunbd.ttf")
F_REG = os.path.join(FONTS, "malgun.ttf")

# vol001 영구 컬러 시스템
CREAM = (240, 238, 230)        # #F0EEE6
DARK_BG = (10, 10, 10)         # #0a0a0a (검정 반전)
DARK = (25, 25, 25)            # #191919
GRAY = (128, 112, 96)          # #807060
LINE = (208, 200, 188)         # #D0C8BC (가로선)
BROWN = (204, 120, 92)         # #CC785C (Crail Brown)
WHITE = (255, 255, 255)
LIGHT_BROWN = (255, 245, 236)  # #FFF5EC


def draw_star(draw, cx, cy, size, color, width=2):
    """✷ 별 직접 그림 (PIL은 색상 이모지 미지원)"""
    half = size // 2
    quarter = size // 4
    # 십자
    draw.line([(cx, cy - half), (cx, cy + half)], fill=color, width=width)
    draw.line([(cx - half, cy), (cx + half, cy)], fill=color, width=width)
    # X
    draw.line([(cx - quarter, cy - quarter), (cx + quarter, cy + quarter)], fill=color, width=width)
    draw.line([(cx - quarter, cy + quarter), (cx + quarter, cy - quarter)], fill=color, width=width)


def draw_header_labels(draw, vol, date_str, day_name, badge_text):
    """vol001 표준 상단 라벨 (좌: 메타, 우: 강조 박스)"""
    f_label = ImageFont.truetype(F_BOLD, 22)
    f_badge = ImageFont.truetype(F_BOLD, 22)

    # 좌측 라벨
    draw.text((80, 75), f"{vol} — {date_str} · {day_name}", fill=DARK, font=f_label)

    # 우측 강조 배지 (Crail Brown 둥근 박스)
    badge_w = len(badge_text) * 14 + 60
    bx, by = 1080 - badge_w - 80, 65
    draw.rounded_rectangle([(bx, by), (bx + badge_w, by + 50)], radius=25, fill=BROWN)
    draw.text((bx + 25, by + 12), badge_text, fill=WHITE, font=f_badge)
    # 별
    draw_star(draw, bx + badge_w - 22, by + 25, 14, WHITE, width=2)


def draw_footer(draw, slide_num, total, dot_indicator=True):
    """vol001 표준 하단 (별 + 가로선 + 카운터 + 슬라이드 인디케이터)"""
    f_counter = ImageFont.truetype(F_REG, 20)

    # 큰 별 (Crail Brown, 좌측)
    draw_star(draw, 110, 920, 50, BROWN, width=3)

    # 가로선
    draw.line([(80, 970), (1000, 970)], fill=LINE, width=1)

    # 카운터 (우측)
    draw.text((780, 1010), f"{slide_num}/{total} · @bella_ai_auto", fill=DARK, font=f_counter)

    # 슬라이드 인디케이터 (중앙) ●●●●
    if dot_indicator:
        cx_start = 410
        for i in range(total):
            cx = cx_start + i * 25
            color = DARK if i == slide_num - 1 else (200, 192, 180)
            draw.ellipse([(cx, 1015), (cx + 8, 1023)], fill=color)


def slide_1(out, vol="VOL.003", date_str="2026.04.28", day_name="TUESDAY", badge="WEEK 1 ✦"):
    """Hook — 거대 한글 + 숫자 Crail Brown"""
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(F_BOLD, 92)
    f_sub = ImageFont.truetype(F_BOLD, 36)

    draw_header_labels(d, vol, date_str, day_name, "FIRST POST")

    # 메인 4줄 (숫자만 Crail Brown 강조)
    # "Claude Skills 4종 +" / "MCP 3 시스템 =" / "20명 페르소나" / "24/7 자동"
    y = 240
    # Line 1: "Claude Skills " + "4종" (BROWN) + " +"
    d.text((80, y), "Claude Skills ", fill=DARK, font=f_huge)
    # 측정해서 위치 잡기
    skills_w = d.textlength("Claude Skills ", font=f_huge)
    d.text((80 + skills_w, y), "4종", fill=BROWN, font=f_huge)
    skills_w2 = d.textlength("Claude Skills 4종", font=f_huge)
    d.text((80 + skills_w2, y), " +", fill=DARK, font=f_huge)

    y += 110
    # Line 2: "MCP " + "3" (BROWN) + " 시스템 ="
    d.text((80, y), "MCP ", fill=DARK, font=f_huge)
    mcp_w = d.textlength("MCP ", font=f_huge)
    d.text((80 + mcp_w, y), "3", fill=BROWN, font=f_huge)
    mcp_w2 = d.textlength("MCP 3", font=f_huge)
    d.text((80 + mcp_w2, y), " 시스템 =", fill=DARK, font=f_huge)

    y += 110
    # Line 3: "20명" (BROWN) + " 페르소나"
    d.text((80, y), "20명", fill=BROWN, font=f_huge)
    p_w = d.textlength("20명", font=f_huge)
    d.text((80 + p_w, y), " 페르소나", fill=DARK, font=f_huge)

    y += 110
    # Line 4: "24/7 자동"
    d.text((80, y), "24/7 자동", fill=DARK, font=f_huge)

    # 부제 (Crail Brown 이탤릭 톤)
    d.text((80, 720), "비개발자 1명, 매주 6편 운영 라이브 ✷", fill=BROWN, font=f_sub)

    draw_footer(d, 1, 4)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_2(out):
    """Three Bots — 3개 봇 시스템 (vol001 slide 3 패턴)"""
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(F_BOLD, 76)
    f_label = ImageFont.truetype(F_BOLD, 22)
    f_card_name = ImageFont.truetype(F_BOLD, 38)
    f_card_desc = ImageFont.truetype(F_REG, 24)
    f_card_sub = ImageFont.truetype(F_REG, 20)
    f_box = ImageFont.truetype(F_BOLD, 30)

    draw_header_labels(d, "VOL.003", "2026.04.28", "TUESDAY", "THE TEAM")

    # 메인 헤드라인 2줄
    d.text((80, 220), "3개의 24/7", fill=DARK, font=f_huge)
    d.text((80, 305), "봇 시스템", fill=DARK, font=f_huge)

    # 3 카드 세로
    cards = [
        ("☁️ 만능이", "Claude API · Slack Bolt", "Mac mini launchd 24/7", BROWN),
        ("🐹 햄스터즈", "Claude Code · 12 페르소나 자동", "윈도우 데스크탑 + 노트북", DARK),
        ("🐕 퍼피즈", "OpenClaw · 6 페르소나 자동", "Mac mini launchd", DARK),
    ]
    y = 460
    for i, (name, desc1, desc2, color) in enumerate(cards):
        # 좌측 컬러 바
        d.rectangle([(80, y), (88, y + 110)], fill=BROWN)
        # 이름
        d.text((110, y + 5), name, fill=DARK, font=f_card_name)
        # 디스크립션
        d.text((110, y + 55), desc1, fill=GRAY, font=f_card_desc)
        d.text((110, y + 82), desc2, fill=GRAY, font=f_card_sub)
        y += 130

    # 임팩트 박스 (Crail Brown)
    d.rounded_rectangle([(80, 850), (1000, 920)], radius=8, fill=BROWN)
    d.text((110, 870), "역할 자동 전환, 사람은 단 1명", fill=WHITE, font=f_box)

    draw_footer(d, 2, 4)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_3(out):
    """Trends — Claude Skills + MCP 핵심 메시지"""
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(F_BOLD, 76)
    f_check = ImageFont.truetype(F_BOLD, 32)
    f_sub = ImageFont.truetype(F_REG, 26)

    draw_header_labels(d, "VOL.003", "2026.04.28", "TUESDAY", "THIS WEEK")

    d.text((80, 220), "이번 주 진짜", fill=DARK, font=f_huge)
    d.text((80, 305), "쓰는 트렌드", fill=DARK, font=f_huge)
    d.text((80, 390), "2가지", fill=BROWN, font=f_huge)

    # 2 트렌드 박스
    items = [
        ("01", "Claude Skills", "프롬프트 안 써도 자동 호출", "폴더만 만들면 끝, 5분 컷"),
        ("02", "MCP", "Model Context Protocol", "비개발자 1명이 20명 페르소나 운영"),
    ]
    y = 540
    for num, title, desc1, desc2 in items:
        # 큰 숫자 (Crail Brown)
        d.text((80, y), num, fill=BROWN, font=f_huge)
        # 타이틀
        d.text((220, y + 5), title, fill=DARK, font=f_check)
        # 설명
        d.text((220, y + 50), desc1, fill=GRAY, font=f_sub)
        d.text((220, y + 80), desc2, fill=GRAY, font=f_sub)
        y += 160

    draw_footer(d, 3, 4)
    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


def slide_4(out):
    """CTA — 댓글 DREAMTEAM (Crail Brown 풀 박스)"""
    img = Image.new('RGB', (1080, 1080), BROWN)
    d = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(F_BOLD, 22)
    f_huge = ImageFont.truetype(F_BOLD, 80)
    f_handle = ImageFont.truetype(F_BOLD, 56)
    f_box = ImageFont.truetype(F_BOLD, 30)
    f_sub = ImageFont.truetype(F_REG, 24)

    # 상단 라벨 (흰 박스)
    d.rounded_rectangle([(80, 65), (380, 115)], radius=25, outline=WHITE, width=2)
    d.text((110, 78), "FOLLOW THE JOURNEY", fill=WHITE, font=f_label)

    # 우측 별
    draw_star(d, 1010, 90, 30, WHITE, width=2)

    # 메인
    d.text((110, 230), "댓글에", fill=WHITE, font=f_huge)
    d.text((110, 330), "「DREAMTEAM」", fill=WHITE, font=f_huge)
    d.text((110, 430), "남기시면 ✷", fill=WHITE, font=f_huge)

    # 가벼운 약속 박스 (흰 테두리)
    d.rounded_rectangle([(110, 600), (970, 800)], radius=14, outline=WHITE, width=3)
    promises = [
        "드림팀 한 장 소개 PNG",
        "매주 6일 시리즈 캘린더",
        "Claude Skills 가이드 PDF",
    ]
    y = 625
    for p in promises:
        # 체크 표시 직접 그림
        d.line([(150, y + 25), (165, y + 40)], fill=WHITE, width=4)
        d.line([(165, y + 40), (185, y + 15)], fill=WHITE, width=4)
        d.text((215, y + 5), p, fill=WHITE, font=f_box)
        y += 60

    # 하단 핸들 + 가로선
    d.line([(80, 880), (1000, 880)], fill=WHITE, width=1)
    d.text((110, 905), "@bella_ai_auto", fill=WHITE, font=f_handle)
    d.text((780, 1010), "4/4 · @bella_ai_auto", fill=WHITE, font=ImageFont.truetype(F_REG, 20))

    img.save(out, 'PNG', optimize=True)
    print(f'[OK] {out.name}')


if __name__ == '__main__':
    out_dir = Path('D:/bella-ai-intel/public_assets/instagram')
    out_dir.mkdir(parents=True, exist_ok=True)

    slide_1(out_dir / 'vol003_v2_ko_1.png')
    slide_2(out_dir / 'vol003_v2_ko_2.png')
    slide_3(out_dir / 'vol003_v2_ko_3.png')
    slide_4(out_dir / 'vol003_v2_ko_4.png')
    print('\n[DONE] vol003_v2 KO 4장 (vol001 톤 풀 적용)')

"""KO/ZH/EN Skill List 1080x1080 PNG (PIL Pretendard 직접 합성, 한글 깨짐 0%)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# Pretendard 또는 맑은 고딕 폴백
FONTS_DIR = "C:/Windows/Fonts"
FONT_KR_BOLD = os.path.join(FONTS_DIR, "malgunbd.ttf")
FONT_KR_REG = os.path.join(FONTS_DIR, "malgun.ttf")

CREAM = (240, 238, 230)
BROWN = (204, 120, 92)
DARK = (25, 25, 25)
GRAY = (128, 112, 96)
WHITE = (255, 255, 255)
LIGHT_BROWN = (255, 245, 236)


def make_png(filename: str, data: dict, lang_code: str):
    """1080x1080 PNG 생성"""
    img = Image.new('RGB', (1080, 1080), CREAM)
    d = ImageDraw.Draw(img)

    # 폰트 크기별 인스턴스
    f_label = ImageFont.truetype(FONT_KR_BOLD, 28)
    f_h1 = ImageFont.truetype(FONT_KR_BOLD, 64)
    f_sub = ImageFont.truetype(FONT_KR_REG, 26)
    f_h2 = ImageFont.truetype(FONT_KR_BOLD, 38)
    f_body = ImageFont.truetype(FONT_KR_REG, 28)
    f_step = ImageFont.truetype(FONT_KR_REG, 24)
    f_cta = ImageFont.truetype(FONT_KR_BOLD, 26)
    f_cta_sub = ImageFont.truetype(FONT_KR_REG, 22)
    f_footer = ImageFont.truetype(FONT_KR_REG, 18)

    # 상단 라벨 박스
    d.rounded_rectangle([(70, 60), (520, 110)], radius=8, fill=BROWN)
    d.text((90, 70), data['label'], fill=WHITE, font=f_label)

    # 메인 헤드라인
    d.text((70, 165), data['title_line1'], fill=DARK, font=f_h1)
    d.text((70, 245), data['title_line2'], fill=DARK, font=f_h1)

    # 부제
    d.text((70, 340), data['subtitle'], fill=BROWN, font=f_sub)

    # ━━━━━━ 구분선
    d.rectangle([(70, 395), (200, 401)], fill=BROWN)

    # Skills 섹션
    d.text((70, 425), data['skills_header'], fill=DARK, font=f_h2)
    y = 495
    for skill in data['skills']:
        d.ellipse([(75, y + 10), (95, y + 30)], fill=BROWN)
        d.text((110, y), skill, fill=DARK, font=f_body)
        y += 50

    # Custom Skill 섹션
    y += 20
    d.text((70, y), data['custom_header'], fill=DARK, font=f_h2)
    y += 60
    for step in data['custom_steps']:
        d.text((85, y), step, fill=GRAY, font=f_step)
        y += 38

    # CTA Box (Crail Brown)
    y += 15
    d.rounded_rectangle([(70, y), (1010, y + 90)], radius=12, fill=BROWN)
    d.text((90, y + 12), data['cta_line1'], fill=WHITE, font=f_cta)
    d.text((90, y + 50), data['cta_line2'], fill=WHITE, font=f_cta_sub)

    # Footer
    d.text((70, 1010), data['footer'], fill=GRAY, font=f_footer)
    d.text((720, 1010), '@bella_ai_auto · ✷', fill=BROWN, font=f_footer)

    # 저장
    out_dir = Path('D:/bella-ai-intel/public_assets/pdfs')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    img.save(out_path, 'PNG', optimize=True)
    print(f'[OK] {filename} ({out_path.stat().st_size:,} bytes)')


KO = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 가이드',
    'title_line2': '5분 안에 시작하기',
    'subtitle': '비개발자 1인 + 3봇 시스템 = 20명 24/7 운영',
    'skills_header': '📚 무료 Skill 4종 (claude.ai 즉시 사용)',
    'skills': [
        'Excel — 데이터 분석 · 차트 자동',
        'Word — 문서 자동 작성 · 편집',
        'PowerPoint — 프레젠테이션 즉시',
        'PDF — 보고서 자동 생성',
    ],
    'custom_header': '🛠 Custom Skill 5분 만들기',
    'custom_steps': [
        '1. claude.ai → 설정 → 기능',
        '2. SKILL.md 파일 작성 (frontmatter + 본문)',
        '3. ZIP 압축 → 업로드',
        '4. 다음 대화부터 자동 적용 ✨',
    ],
    'cta_line1': '🎁 매주 6회 시리즈 받아보기',
    'cta_line2': '월 Claude / 화 트렌드 / 수 드림팀 / 목 튜토리얼 / 금 MCP / 토 SecondBrain',
    'footer': '벨라의 둥지 — AI 드림팀 허브',
}

ZH = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 指南',
    'title_line2': '5 分鐘上手',
    'subtitle': '1 位非開發者 + 3 機器人系統 = 20 個角色 24/7',
    'skills_header': '📚 免費 Skill 4 種 (claude.ai 即用)',
    'skills': [
        'Excel — 資料分析 · 自動圖表',
        'Word — 自動文件撰寫 · 編輯',
        'PowerPoint — 立即製作簡報',
        'PDF — 自動生成報告',
    ],
    'custom_header': '🛠 5 分鐘做出自己的 Skill',
    'custom_steps': [
        '1. claude.ai → 設定 → 功能',
        '2. 編寫 SKILL.md (frontmatter + 內文)',
        '3. ZIP 壓縮 → 上傳',
        '4. 下次對話自動應用 ✨',
    ],
    'cta_line1': '🎁 每週 6 次系列接收',
    'cta_line2': '一 Claude / 二 趨勢 / 三 夢想團隊 / 四 教學 / 五 MCP / 六 SecondBrain',
    'footer': 'Bella 的小窩 — AI 夢想團隊',
}

EN = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills Guide',
    'title_line2': 'Start in 5 Minutes',
    'subtitle': '1 non-dev + 3 bot systems = 20 personas 24/7',
    'skills_header': '📚 4 Free Skills (claude.ai instant)',
    'skills': [
        'Excel — data analysis · auto charts',
        'Word — drafting · editing',
        'PowerPoint — instant slides',
        'PDF — auto report generation',
    ],
    'custom_header': '🛠 Build Your Own Skill in 5 min',
    'custom_steps': [
        '1. claude.ai → Settings → Features',
        '2. Write SKILL.md (frontmatter + body)',
        '3. ZIP it → Upload',
        '4. Auto-applied from next chat ✨',
    ],
    'cta_line1': '🎁 Weekly 6-day series',
    'cta_line2': 'Mon Claude / Tue Trends / Wed Dream Team / Thu Tutorial / Fri MCP / Sat SecondBrain',
    'footer': "Bella's Nest — AI Dream Team Hub",
}


if __name__ == '__main__':
    make_png('dreamteam_skill_list_ko.png', KO, 'ko')
    make_png('dreamteam_skill_list_zh.png', ZH, 'zh')
    make_png('dreamteam_skill_list_en.png', EN, 'en')
    print('\n[DONE] 3 Skill List PNGs generated')

"""KO/ZH/EN 1페이지 무료 Skill 리스트 PDF 생성"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록 (Pretendard 폴백 맑은 고딕)
fonts_dir = "C:/Windows/Fonts"
for f in ['malgunbd.ttf', 'malgun.ttf']:
    p = os.path.join(fonts_dir, f)
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont('KR', p))
        FONT_KR = 'KR'
        print(f'[OK] Korean font: {f}')
        break
else:
    FONT_KR = 'Helvetica'

CREAM = HexColor('#F0EEE6')
BROWN = HexColor('#CC785C')
DARK = HexColor('#191919')
GRAY = HexColor('#807060')
WHITE = HexColor('#ffffff')


def make_pdf(filename, data, font='KR'):
    out_dir = Path('D:/bella-ai-intel/public_assets/pdfs')
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    W, H = A4

    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # 라벨
    c.setFillColor(BROWN)
    c.rect(2*cm, H - 2.2*cm, 7*cm, 0.7*cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(font, 11)
    c.drawString(2.2*cm, H - 1.85*cm, data['label'])

    # 헤드라인
    c.setFillColor(DARK)
    c.setFont(font, 28)
    c.drawString(2*cm, H - 4*cm, data['title_line1'])
    c.drawString(2*cm, H - 5.2*cm, data['title_line2'])

    # 부제
    c.setFillColor(BROWN)
    c.setFont(font, 13)
    c.drawString(2*cm, H - 6*cm, data['subtitle'])

    # Skills
    y = H - 8*cm
    c.setFillColor(DARK)
    c.setFont(font, 16)
    c.drawString(2*cm, y, data['skills_header'])
    y -= 1*cm
    for skill in data['skills']:
        c.setFillColor(BROWN)
        c.circle(2.3*cm, y - 0.15*cm, 0.15*cm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont(font, 12)
        c.drawString(2.7*cm, y - 0.2*cm, skill)
        y -= 0.7*cm

    # Custom
    y -= 0.5*cm
    c.setFillColor(DARK)
    c.setFont(font, 16)
    c.drawString(2*cm, y, data['custom_header'])
    y -= 0.8*cm
    for step in data['custom_steps']:
        c.setFillColor(GRAY)
        c.setFont(font, 11)
        c.drawString(2.3*cm, y, step)
        y -= 0.55*cm

    # CTA Box
    y -= 0.5*cm
    c.setFillColor(BROWN)
    c.rect(2*cm, y - 0.3*cm, W - 4*cm, 1.5*cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(font, 12)
    c.drawString(2.3*cm, y + 0.7*cm, data['cta_line1'])
    c.drawString(2.3*cm, y + 0.1*cm, data['cta_line2'])

    # Footer
    c.setFillColor(GRAY)
    c.setFont(font, 9)
    c.drawString(2*cm, 1.5*cm, data['footer'])
    c.drawRightString(W - 2*cm, 1.5*cm, '@bella_ai_auto · bella-nest.vercel.app')
    c.save()
    print(f'[OK] {filename} ({out.stat().st_size:,} bytes)')


KO = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 가이드',
    'title_line2': '5분 안에 시작하기',
    'subtitle': '비개발자 1인 + 3봇 시스템 = 20명 24/7 운영',
    'skills_header': '무료 Skill 4종 (claude.ai 즉시 사용)',
    'skills': [
        'Excel - 데이터 분석 차트 자동 생성',
        'Word - 문서 자동 작성 편집',
        'PowerPoint - 프레젠테이션 즉시 만들기',
        'PDF - 보고서 자동 생성',
    ],
    'custom_header': 'Custom Skill 5분 만들기',
    'custom_steps': [
        '1. claude.ai - 설정 - 기능',
        '2. SKILL.md 파일 작성 (YAML frontmatter + 본문)',
        '3. ZIP 압축 - 업로드',
        '4. 다음 대화부터 자동 적용',
    ],
    'cta_line1': '매주 6회 시리즈 받아보기 - 팔로우 + 알림 ON',
    'cta_line2': '월 Claude / 화 트렌드 / 수 드림팀 / 목 튜토리얼 / 금 MCP / 토 SecondBrain',
    'footer': '벨라의 둥지 - AI 드림팀 허브 매일 발행',
}

ZH = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 指南',
    'title_line2': '5 分鐘上手',
    'subtitle': '1 位非開發者 + 3 機器人系統 = 20 個角色 24/7 運營',
    'skills_header': '免費 Skill 4 種 (claude.ai 即用)',
    'skills': [
        'Excel - 資料分析 自動圖表',
        'Word - 自動文件撰寫 編輯',
        'PowerPoint - 立即製作簡報',
        'PDF - 自動生成報告',
    ],
    'custom_header': '5 分鐘做出自己的 Skill',
    'custom_steps': [
        '1. claude.ai - 設定 - 功能',
        '2. 編寫 SKILL.md',
        '3. ZIP 壓縮 - 上傳',
        '4. 下次對話自動應用',
    ],
    'cta_line1': '每週 6 次系列 - 追蹤 + 開啟通知',
    'cta_line2': '一 Claude / 二 趨勢 / 三 夢想團隊 / 四 教學 / 五 MCP / 六 SecondBrain',
    'footer': 'Bella 的小窩 - AI 夢想團隊中心 每日發布',
}

EN = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills Guide',
    'title_line2': 'Start in 5 Minutes',
    'subtitle': '1 non-dev + 3 bot systems = 20 personas 24/7',
    'skills_header': '4 Free Skills (claude.ai instant)',
    'skills': [
        'Excel - data analysis auto charts',
        'Word - drafting editing',
        'PowerPoint - instant slides',
        'PDF - auto report',
    ],
    'custom_header': 'Build Your Own Skill in 5 min',
    'custom_steps': [
        '1. claude.ai - Settings - Features',
        '2. Write SKILL.md',
        '3. ZIP it - Upload',
        '4. Auto-applied from next chat',
    ],
    'cta_line1': 'Weekly 6-day series - Follow + Notifications ON',
    'cta_line2': 'Mon Claude / Tue Trends / Wed Dream Team / Thu Tutorial / Fri MCP / Sat SecondBrain',
    'footer': "Bella's Nest - AI Dream Team Hub Daily",
}


if __name__ == '__main__':
    make_pdf('dreamteam_skill_list_ko.pdf', KO)
    make_pdf('dreamteam_skill_list_zh.pdf', ZH)
    make_pdf('dreamteam_skill_list_en.pdf', EN, font='Helvetica')
    print('\n[DONE] 3 PDFs generated')

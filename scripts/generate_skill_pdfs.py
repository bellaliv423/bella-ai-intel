"""
KO/ZH/EN 멀티페이지 Claude Skills 가이드 PDF
- 페이지 1: 표지 + 무료 Skill 4종
- 페이지 2: 5분 만들기 단계 + SKILL.md 예시 코드
- 페이지 3: 실전 프롬프트 예시 + CTA
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = "C:/Windows/Fonts"
for f in ['malgunbd.ttf', 'malgun.ttf']:
    p = os.path.join(FONTS, f)
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont('KR', p))
        FONT_KR = 'KR'
        break
else:
    FONT_KR = 'Helvetica'

# 코드 폰트 (mono)
for f in ['consola.ttf', 'cour.ttf']:
    p = os.path.join(FONTS, f)
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont('MONO', p))
        FONT_MONO = 'MONO'
        break
else:
    FONT_MONO = 'Courier'

CREAM = HexColor('#F0EEE6')
BROWN = HexColor('#CC785C')
DARK = HexColor('#191919')
GRAY = HexColor('#807060')
WHITE = HexColor('#ffffff')
CODE_BG = HexColor('#1F1F1F')
CODE_TEXT = HexColor('#E8E6DE')
LIGHT_BROWN = HexColor('#FFF5EC')


def page_bg(c, W, H):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def label_box(c, y_top, text, W):
    c.setFillColor(BROWN)
    c.rect(2*cm, y_top - 0.7*cm, 7*cm, 0.7*cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_KR, 11)
    c.drawString(2.2*cm, y_top - 0.5*cm, text)


def page_footer(c, W, page_num, total):
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.3)
    c.line(2*cm, 1.5*cm, W - 2*cm, 1.5*cm)
    c.setFillColor(GRAY)
    c.setFont(FONT_KR, 8)
    c.drawString(2*cm, 1.1*cm, f'벨라의 둥지 — bella-nest.vercel.app/team')
    c.drawRightString(W - 2*cm, 1.1*cm, f'@bella_ai_auto · {page_num}/{total}')


def make_pdf(filename: str, data: dict, font_kr=FONT_KR):
    out_dir = Path('D:/bella-ai-intel/public_assets/pdfs')
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / filename
    c = canvas.Canvas(str(out), pagesize=A4)
    W, H = A4
    fk = font_kr
    TOTAL = 3

    # ━━━━━━━━━━━━━━━━━ PAGE 1: 표지 + Skill 4종 ━━━━━━━━━━━━━━━━━
    page_bg(c, W, H)
    label_box(c, H - 1.5*cm, data['label'], W)

    c.setFillColor(DARK); c.setFont(fk, 28)
    c.drawString(2*cm, H - 4*cm, data['title_line1'])
    c.drawString(2*cm, H - 5.2*cm, data['title_line2'])

    c.setFillColor(BROWN); c.setFont(fk, 13)
    c.drawString(2*cm, H - 6*cm, data['subtitle'])

    c.setStrokeColor(BROWN); c.setLineWidth(2)
    c.line(2*cm, H - 6.7*cm, 5*cm, H - 6.7*cm)

    # Skill 4종
    y = H - 8*cm
    c.setFillColor(DARK); c.setFont(fk, 16)
    c.drawString(2*cm, y, data['skills_header'])
    y -= 1*cm
    for skill in data['skills']:
        c.setFillColor(BROWN)
        c.circle(2.3*cm, y - 0.15*cm, 0.18*cm, fill=1, stroke=0)
        c.setFillColor(DARK); c.setFont(fk, 12)
        c.drawString(2.8*cm, y - 0.2*cm, skill)
        y -= 0.85*cm

    # 페이지 1 푸터
    y -= 0.5*cm
    c.setFillColor(LIGHT_BROWN)
    c.rect(2*cm, y - 0.3*cm, W - 4*cm, 1.6*cm, fill=1, stroke=0)
    c.setFillColor(BROWN); c.setFont(fk, 12)
    c.drawString(2.3*cm, y + 0.7*cm, data['page1_quote_1'])
    c.setFillColor(DARK); c.setFont(fk, 10)
    c.drawString(2.3*cm, y + 0.1*cm, data['page1_quote_2'])

    page_footer(c, W, 1, TOTAL)
    c.showPage()

    # ━━━━━━━━━━━━━━━━━ PAGE 2: 5분 만들기 + 예시 코드 ━━━━━━━━━━━━━━━━━
    page_bg(c, W, H)
    label_box(c, H - 1.5*cm, data['label'], W)

    c.setFillColor(DARK); c.setFont(fk, 22)
    c.drawString(2*cm, H - 3.5*cm, data['p2_title'])

    c.setFillColor(GRAY); c.setFont(fk, 12)
    c.drawString(2*cm, H - 4.3*cm, data['p2_subtitle'])

    # 5단계
    y = H - 5.5*cm
    for i, step in enumerate(data['custom_steps_full'], 1):
        c.setFillColor(BROWN); c.setFont(fk, 14)
        c.drawString(2*cm, y, f'{i}.')
        c.setFillColor(DARK); c.setFont(fk, 12)
        c.drawString(2.7*cm, y, step['title'])
        if step.get('desc'):
            c.setFillColor(GRAY); c.setFont(fk, 10)
            c.drawString(2.7*cm, y - 0.4*cm, step['desc'])
            y -= 1.1*cm
        else:
            y -= 0.7*cm

    # SKILL.md 예시 코드 박스
    y -= 0.2*cm
    c.setFillColor(DARK); c.setFont(fk, 13)
    c.drawString(2*cm, y, data['code_label'])
    y -= 0.5*cm

    code_lines = data['skill_md_example']
    code_h = len(code_lines) * 0.45*cm + 0.4*cm
    c.setFillColor(CODE_BG)
    c.rect(2*cm, y - code_h, W - 4*cm, code_h, fill=1, stroke=0)
    cy = y - 0.5*cm
    for line in code_lines:
        c.setFillColor(CODE_TEXT)
        c.setFont(FONT_MONO, 9)
        c.drawString(2.3*cm, cy, line)
        cy -= 0.45*cm

    page_footer(c, W, 2, TOTAL)
    c.showPage()

    # ━━━━━━━━━━━━━━━━━ PAGE 3: 프롬프트 예시 + CTA ━━━━━━━━━━━━━━━━━
    page_bg(c, W, H)
    label_box(c, H - 1.5*cm, data['label'], W)

    c.setFillColor(DARK); c.setFont(fk, 22)
    c.drawString(2*cm, H - 3.5*cm, data['p3_title'])

    c.setFillColor(GRAY); c.setFont(fk, 12)
    c.drawString(2*cm, H - 4.3*cm, data['p3_subtitle'])

    # 프롬프트 예시 3개
    y = H - 5.5*cm
    for i, ex in enumerate(data['prompt_examples'], 1):
        c.setFillColor(BROWN); c.setFont(fk, 13)
        c.drawString(2*cm, y, f'#{i} {ex["title"]}')
        y -= 0.5*cm

        # 프롬프트 박스
        prompt_lines = ex['prompt']
        box_h = len(prompt_lines) * 0.42*cm + 0.4*cm
        c.setFillColor(LIGHT_BROWN)
        c.rect(2*cm, y - box_h, W - 4*cm, box_h, fill=1, stroke=0)
        py = y - 0.4*cm
        for line in prompt_lines:
            c.setFillColor(DARK)
            c.setFont(fk, 10)
            c.drawString(2.3*cm, py, line)
            py -= 0.42*cm
        y -= box_h + 0.6*cm

    # 마지막 CTA
    y -= 0.3*cm
    c.setFillColor(BROWN)
    c.rect(2*cm, y - 1.5*cm, W - 4*cm, 1.5*cm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(fk, 13)
    c.drawString(2.3*cm, y - 0.5*cm, data['cta_line1'])
    c.setFont(fk, 10)
    c.drawString(2.3*cm, y - 1*cm, data['cta_line2'])

    page_footer(c, W, 3, TOTAL)
    c.save()
    print(f'[OK] {filename} ({out.stat().st_size:,} bytes)')


# ════════════════════════ KO ════════════════════════
KO = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 가이드',
    'title_line2': '5분 안에 시작하기',
    'subtitle': '비개발자 1인 + 3봇 시스템 = 20명 24/7 운영',
    'skills_header': '📚 무료 Skill 4종 (claude.ai 즉시 사용)',
    'skills': [
        'Excel — 데이터 분석 · 차트 자동 생성',
        'Word — 문서 자동 작성 · 편집',
        'PowerPoint — 프레젠테이션 즉시 만들기',
        'PDF — 보고서 자동 생성',
    ],
    'page1_quote_1': '💡 4종은 claude.ai 무료/Pro 사용자 모두 즉시 활성화',
    'page1_quote_2': '설정 → 기능 → Skills 토글 ON만 하면 끝!',

    'p2_title': 'Custom Skill 5분 만들기',
    'p2_subtitle': '내 업무에 딱 맞는 AI 자동화를 5분 안에',
    'custom_steps_full': [
        {'title': 'claude.ai → 설정 → 기능 → Skills', 'desc': '왼쪽 사이드바 「설정」 → 「기능」 → Skills 섹션'},
        {'title': '「Create new Skill」 클릭', 'desc': 'SKILL.md 편집기 열림 (또는 ZIP 업로드 옵션)'},
        {'title': 'YAML frontmatter 작성 (name + description)', 'desc': '아래 예시 참고 — 가장 중요한 부분'},
        {'title': '본문 작성 (마크다운, 무엇을 어떻게 할지)', 'desc': '단계별 가이드 + 예시 + 주의사항'},
        {'title': '저장 → 다음 대화부터 자동 적용 ✨', 'desc': '관련 키워드 입력 시 Claude가 자동으로 Skill 호출'},
    ],
    'code_label': '📝 SKILL.md 예시 (실제 사용 가능)',
    'skill_md_example': [
        '---',
        'name: my-weekly-report',
        'description: 매주 금요일 회사 주간보고 자동 작성. 형식 통일',
        '  + 이번 주 한 일/다음 주 계획/이슈 3섹션. 사용 시점:',
        '  "주간보고 작성", "이번 주 보고서" 요청 시.',
        '---',
        '',
        '# 주간보고 작성 가이드',
        '',
        '## 형식',
        '1. 이번 주 한 일 (불릿 5개)',
        '2. 다음 주 계획 (불릿 3개)',
        '3. 이슈/도움 필요 (있으면)',
        '',
        '## 톤',
        '- 간결, 사실 기반',
        '- 정량적 수치 포함 (예: 매출 +15%)',
    ],

    'p3_title': '실전 프롬프트 예시 3종',
    'p3_subtitle': 'Skill 활성화 후 바로 써보는 명령',
    'prompt_examples': [
        {
            'title': 'Excel Skill — 매출 데이터 분석',
            'prompt': [
                '"sales.xlsx 첨부했어요.',
                '월별 매출 추이 + 카테고리별 비중',
                '+ 다음 달 예측 그래프 만들어주세요"',
            ],
        },
        {
            'title': 'PowerPoint Skill — 발표 자료 즉시',
            'prompt': [
                '"이 보고서를 10장짜리 발표 PPT로 만들어주세요.',
                'Anthropic 브랜드 톤(크림+브라운).',
                '1장: 표지 / 2-9: 본문 / 10: Q&A"',
            ],
        },
        {
            'title': 'Custom Skill — 내 업무 자동화',
            'prompt': [
                '"오늘의 업무일지 작성해줘"',
                '→ 미리 만든 my-worklog Skill이 자동 호출',
                '→ 형식·톤 그대로 자동 작성 ✨',
            ],
        },
    ],
    'cta_line1': '🎁 매주 6회 시리즈 — 팔로우 + 알림 ON으로 받아보기',
    'cta_line2': '월 Claude / 화 트렌드 / 수 드림팀 / 목 튜토리얼 / 금 MCP / 토 SecondBrain',
}

# ════════════════════════ ZH ════════════════════════
ZH = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills 指南',
    'title_line2': '5 分鐘上手',
    'subtitle': '1 位非開發者 + 3 機器人系統 = 20 個角色 24/7 運營',
    'skills_header': '📚 免費 Skill 4 種 (claude.ai 即用)',
    'skills': [
        'Excel — 資料分析 · 自動圖表',
        'Word — 自動文件撰寫 · 編輯',
        'PowerPoint — 立即製作簡報',
        'PDF — 自動生成報告',
    ],
    'page1_quote_1': '💡 4 種免費/Pro 用戶都可立即啟用',
    'page1_quote_2': '設定 → 功能 → Skills 開關 ON 即可！',

    'p2_title': '5 分鐘做出自己的 Skill',
    'p2_subtitle': '為自己的工作量身打造 AI 自動化',
    'custom_steps_full': [
        {'title': 'claude.ai → 設定 → 功能 → Skills', 'desc': '左側「設定」→「功能」→ Skills 區塊'},
        {'title': '點選「Create new Skill」', 'desc': '開啟 SKILL.md 編輯器（或 ZIP 上傳）'},
        {'title': '撰寫 YAML frontmatter (name + description)', 'desc': '參考下方範例 — 最關鍵部分'},
        {'title': '撰寫內文 (Markdown，做什麼怎麼做)', 'desc': '步驟指南 + 範例 + 注意事項'},
        {'title': '儲存 → 下次對話自動應用 ✨', 'desc': '輸入相關關鍵字 Claude 自動呼叫 Skill'},
    ],
    'code_label': '📝 SKILL.md 範例 (可立即使用)',
    'skill_md_example': [
        '---',
        'name: my-weekly-report',
        'description: 每週五自動撰寫公司週報。統一格式',
        '  本週完成/下週計畫/問題 3 段。使用時機：',
        '  "撰寫週報" 或 "本週報告" 請求時。',
        '---',
        '',
        '# 週報撰寫指南',
        '',
        '## 格式',
        '1. 本週完成事項 (5 點)',
        '2. 下週計畫 (3 點)',
        '3. 問題/需協助 (若有)',
        '',
        '## 風格',
        '- 簡潔、事實為主',
        '- 包含量化數字 (例：營收 +15%)',
    ],

    'p3_title': '實戰提示詞範例 3 種',
    'p3_subtitle': 'Skill 啟用後立即使用',
    'prompt_examples': [
        {
            'title': 'Excel Skill — 銷售資料分析',
            'prompt': [
                '"附上 sales.xlsx。',
                '請做月度銷售趨勢 + 分類比重',
                '+ 下月預測圖表"',
            ],
        },
        {
            'title': 'PowerPoint Skill — 簡報立即生成',
            'prompt': [
                '"將此報告做成 10 頁 PPT。',
                'Anthropic 品牌色調 (奶油+棕色)。',
                '1: 封面 / 2-9: 內文 / 10: Q&A"',
            ],
        },
        {
            'title': 'Custom Skill — 工作自動化',
            'prompt': [
                '"撰寫今日工作日誌"',
                '→ 預先建立的 my-worklog Skill 自動呼叫',
                '→ 格式·風格自動套用 ✨',
            ],
        },
    ],
    'cta_line1': '🎁 每週 6 次系列 — 追蹤 + 開啟通知',
    'cta_line2': '一 Claude / 二 趨勢 / 三 夢想團隊 / 四 教學 / 五 MCP / 六 SecondBrain',
}

# ════════════════════════ EN ════════════════════════
EN = {
    'label': 'BELLA AI DREAM TEAM',
    'title_line1': 'Claude Skills Guide',
    'title_line2': 'Start in 5 Minutes',
    'subtitle': '1 non-dev + 3 bot systems = 20 personas 24/7',
    'skills_header': '4 Free Skills (claude.ai instant use)',
    'skills': [
        'Excel - data analysis & auto charts',
        'Word - drafting & editing',
        'PowerPoint - instant slides',
        'PDF - auto report generation',
    ],
    'page1_quote_1': '4 are instantly available for both free/Pro users',
    'page1_quote_2': 'Settings -> Features -> Skills toggle ON, done!',

    'p2_title': 'Build Your Own Skill in 5 Minutes',
    'p2_subtitle': 'AI automation tailored to your exact workflow',
    'custom_steps_full': [
        {'title': 'claude.ai -> Settings -> Features -> Skills', 'desc': 'Sidebar Settings -> Features -> Skills section'},
        {'title': 'Click "Create new Skill"', 'desc': 'Opens SKILL.md editor (or ZIP upload option)'},
        {'title': 'Write YAML frontmatter (name + description)', 'desc': 'See example below - the most critical part'},
        {'title': 'Write the body (markdown, what + how)', 'desc': 'Step-by-step guide + examples + caveats'},
        {'title': 'Save -> Auto-applied from next chat', 'desc': 'Claude auto-invokes Skill on related keywords'},
    ],
    'code_label': 'SKILL.md Example (ready-to-use)',
    'skill_md_example': [
        '---',
        'name: my-weekly-report',
        'description: Auto-writes company weekly reports every Fri.',
        '  Unified format: This week/Next week/Issues 3 sections.',
        '  Trigger: when user asks for "weekly report" or "summary".',
        '---',
        '',
        '# Weekly Report Guide',
        '',
        '## Format',
        '1. This week done (5 bullets)',
        '2. Next week plan (3 bullets)',
        '3. Issues / Help needed (if any)',
        '',
        '## Tone',
        '- Concise, fact-based',
        '- Include quantitative numbers (e.g., revenue +15%)',
    ],

    'p3_title': '3 Real-World Prompt Examples',
    'p3_subtitle': 'Use these immediately after activating the Skill',
    'prompt_examples': [
        {
            'title': 'Excel Skill - Sales data analysis',
            'prompt': [
                '"sales.xlsx attached.',
                'Monthly trend + category breakdown',
                '+ next month forecast chart"',
            ],
        },
        {
            'title': 'PowerPoint Skill - Instant deck',
            'prompt': [
                '"Turn this report into a 10-slide PPT.',
                'Anthropic brand tone (cream+brown).',
                '1: Cover / 2-9: Body / 10: Q&A"',
            ],
        },
        {
            'title': 'Custom Skill - Workflow automation',
            'prompt': [
                '"Write today\'s worklog"',
                '-> my-worklog Skill auto-invoked',
                '-> Format & tone auto-applied',
            ],
        },
    ],
    'cta_line1': 'Weekly 6-day series - Follow + Notifications ON',
    'cta_line2': 'Mon Claude / Tue Trends / Wed Dream Team / Thu Tutorial / Fri MCP / Sat SecondBrain',
}


if __name__ == '__main__':
    make_pdf('dreamteam_skill_list_v2_ko.pdf', KO)
    make_pdf('dreamteam_skill_list_v2_zh.pdf', ZH)
    make_pdf('dreamteam_skill_list_v2_en.pdf', EN, font_kr='Helvetica')
    print('\n[DONE] 3 multi-page PDFs generated (3 pages each)')

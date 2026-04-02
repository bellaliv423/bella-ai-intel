"""
2026-04-02 수동 추가: 오늘 벨라님이 수집한 핵심 뉴스 4건
실행: python scripts/add_today_news.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import get_paths
from collector import load_existing_data, save_data, add_manual_item, create_obsidian_note, translate_item

paths = get_paths()
data = load_existing_data(paths)

# === 1. Claude Code CHANGELOG v2.1.90 (최신!) ===
item1_title = "Claude Code v2.1.90 — /powerup, Auto Mode 경계 존중, 성능 대폭 개선"
data = add_manual_item(data,
    title=item1_title,
    summary_ko="/powerup(인터랙티브 학습), Auto Mode 사용자 경계 존중 수정, SSE 선형시간 처리, SDK 대화 속도 개선, PowerShell 보안 강화. /effort(노력도 조절), /branch(대화 분기), /color(세션 색상), /context(사용량 진단), Ctrl+O 트랜스크립트 검색 등 최신 슬래시 명령어 총정리.",
    summary_zh="/powerup（互動學習）、Auto Mode 尊重用戶邊界修復、SSE 線性時間處理、SDK 對話速度改善、PowerShell 安全強化。/effort（調整深度）、/branch（對話分支）、/color（會話顏色）、/context（用量診斷）等最新斜線命令總整理。",
    source="GitHub CHANGELOG",
    category="claude_code",
    url="https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
)

# === 2. Auto Mode 기술 블로그 ===
item2_title = "Claude Code Auto Mode — 안전한 자동 권한 시스템 (Anthropic 공식)"
data = add_manual_item(data,
    title=item2_title,
    summary_ko="매번 권한 승인 대신 AI 분류기가 자동 판단! 2중 방어(입력층 프롬프트 인젝션 프로브 + 출력층 Sonnet 4.6 트랜스크립트 분류기). 3단계 결정(안전도구→프로젝트내→분류기). FPR 0.4%, FNR 17%. Deny-and-continue로 차단 시 자동 대안 시도. Team 플랜 프리뷰.",
    summary_zh="不再每次批准權限！AI 分類器自動判斷安全性。雙層防禦（輸入層注入探針 + 輸出層 Sonnet 4.6 分類器）。三級決策。FPR 0.4%，FNR 17%。拒絕後自動嘗試安全替代方案。Team 方案預覽。",
    source="Anthropic Engineering Blog",
    category="claude_code",
    url="https://www.anthropic.com/engineering/claude-code-auto-mode"
)

# === 3. 멀티에이전트 하네스 설계 ===
item3_title = "Anthropic 공식 하네스 설계 — GAN 영감 3에이전트(Planner+Generator+Evaluator)"
data = add_manual_item(data,
    title=item3_title,
    summary_ko="Anthropic Labs가 공개한 장시간 자율 코딩 아키텍처. Solo($9,20분)→핵심기능고장 vs 3에이전트($200,6시간)→완성앱! 프론트엔드 평가기준 4가지(Design Quality, Originality, Craft, Functionality). Opus 4.6으로 스프린트 구조 제거 가능. Evaluator는 Playwright MCP로 실제 클릭 테스트.",
    summary_zh="Anthropic Labs 公開的長時間自主編碼架構。Solo($9,20分)→核心功能故障 vs 3代理($200,6小時)→完整應用！前端評估4標準。Opus 4.6 可簡化衝刺結構。評估者用 Playwright MCP 實際點擊測試。",
    source="Anthropic Engineering Blog",
    category="claude_code",
    url="https://www.anthropic.com/engineering/harness-design-long-running-apps"
)

# === 4. Reddit 사용량 최적화 가이드 ===
item4_title = "Claude 사용량 최적화 완벽 가이드 — settings.json으로 60~80% 절감"
data = add_manual_item(data,
    title=item4_title,
    summary_ko="Reddit 모더레이터 정리. settings.json 블록(model:sonnet + MAX_THINKING_TOKENS:10000 + AUTOCOMPACT:50% + SUBAGENT:haiku)으로 60~80% 절감! .claudeignore, CLAUDE.md 60줄 이하, read-once hook, ccusage 모니터링, 하이브리드 전략(Codex+Gemini+Cursor). 피크시간=한국 밤9시~새벽3시.",
    summary_zh="Reddit 版主整理。settings.json 區塊（model:sonnet + MAX_THINKING_TOKENS:10000 + AUTOCOMPACT:50% + SUBAGENT:haiku）節省60~80%！.claudeignore、CLAUDE.md 60行以下、read-once hook、ccusage 監控、混合策略。尖峰時段=韓國晚9點~凌晨3點。",
    source="Reddit r/ClaudeAI Megathread",
    category="claude_code",
    url="https://www.reddit.com/r/ClaudeAI/comments/1pygdbz/usage_limits_bugs_and_performance_discussion/"
)

# Save and create Obsidian notes
save_data(paths, data)

# Create Obsidian notes for each
for item in data["items"][:4]:
    create_obsidian_note(item, paths)

print("\n[DONE] 4건 추가 완료! 대시보드 + 옵시디언 동기화!")

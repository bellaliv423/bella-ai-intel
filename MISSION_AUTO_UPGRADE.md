# BELLA AI Intel - Ambassador Grade Upgrade Mission
# 오토(Auto) 미션: 대시보드 전문가 등급 업그레이드

> **배경**: 벨라님 Claude Community Ambassador 심사 중!
> **목표**: "이 사람은 정말 Claude 전문가다"라는 인상을 주는 대시보드
> **멘토 리뷰**: 2026-03-27 완료, 오토 실행 대기

---

## Phase 1: 수집 소스 확대 (최우선)

### 1-1. Anthropic News (anthropic.com/news)
- **방식**: Next.js `__NEXT_DATA__` JSON 파싱 또는 HTML 직접 파싱
- **참고**: React SSR이라 urllib으로 HTML 받으면 `__NEXT_DATA__` 스크립트 태그에 JSON 포함
- **필드**: title, summary, publishedOn, slug, categories
- **카테고리**: claude_release
- **구현 파일**: `scripts/collector.py` → `collect_from_anthropic_news()` 함수 추가

### 1-2. Claude Code Docs 변경 감지 (code.claude.com)
- **방식**: `https://code.claude.com/docs/llms.txt` 인덱스 파일 활용
- **또는**: urllib + 정규식으로 H1/H2 변경 감지
- **URL 목록**:
  - https://code.claude.com/docs/en/overview
  - https://code.claude.com/docs/ko/chrome
  - https://code.claude.com/docs/ko/best-practices
- **카테고리**: claude_code

### 1-3. Claude API Docs 변경 감지 (platform.claude.com)
- **방식**: urllib + 정규식
- **URL**: https://platform.claude.com/docs/ko/agents-and-tools/tool-use/web-search-tool
- **카테고리**: claude_api

### 1-4. YouTube Anthropic (MCP 활용)
- **도구**: `mcp__claude_ai_youtube_mcp__list_channel_videos`
- **채널**: @anthropic-ai
- **수집**: 최신 영상 제목 + 설명
- **카테고리**: ai_trend 또는 claude_release

### 1-5. Instagram Claude (MCP 활용)
- **도구**: `mcp__claude_ai_Instagram__get_user_media`
- **계정**: claudeai
- **카테고리**: content_sns

### 1-6. X/Twitter + LinkedIn (참조 링크)
- **X**: https://x.com/anthropicai → 스크래핑 불가, 링크 참조만
- **LinkedIn**: https://www.linkedin.com/company/anthropicresearch/posts/ → OAuth 필요, 링크 참조만
- **대시보드에 링크 버튼으로 추가** (수동 확인용)

---

## Phase 2: 품질 개선

### 2-1. 카테고리 자동 분류 정밀화
현재 `auto_categorize()` 키워드가 너무 단순함:
- "claude" → claude_release (Reddit 토론도 전부 여기로 감)
- 추가 필요: "community", "discussion", "question" → ai_trend
- "MCP", "server", "tool" → claude_code
- "price", "plan", "subscription" → claude_release

### 2-2. Reddit 영어 → KO/ZH 자동 요약
- 방안 A: Claude API Haiku로 간단 번역 (비용 낮음)
- 방안 B: 제목만 번역 (본문은 원문 유지)
- 방안 C: 수동 (현실적 한계 인정)
- **추천**: 방안 B (제목 번역만 — 비용 최소, 효과 극대)

### 2-3. 중복 제거 강화
- 같은 뉴스가 Anthropic News + Reddit에서 중복 수집될 수 있음
- title 유사도 비교 (간단한 문자열 매칭)

---

## Phase 3: 전문가 브랜딩 UI

### 3-1. 대시보드 상단 개선
```
"Tracking 8+ Official Sources | Updated Every 6 Hours"
"Powered by BELLA AI Dream Team — Claude Automation Expert"
```

### 3-2. 소스별 아이콘/색상
| 소스 | 아이콘 | 색상 |
|:-----|:------|:-----|
| Anthropic News | 🏢 | #d97757 (웜 러스트) |
| Claude Code Docs | 💻 | #5b8dd9 |
| Claude API Docs | 🔌 | #5a9a72 |
| Reddit | 🔴 | #ff4500 |
| YouTube | ▶️ | #ff0000 |
| Instagram | 📸 | #e4405f |

### 3-3. 헤더에 소셜 링크 바 추가
```html
<div class="source-links">
  <a href="anthropic.com/news">Anthropic</a>
  <a href="reddit.com/r/ClaudeAI">Reddit</a>
  <a href="x.com/anthropicai">X</a>
  <a href="youtube.com/@anthropic-ai">YouTube</a>
  <a href="instagram.com/claudeai">Instagram</a>
  <a href="linkedin.com/company/anthropicresearch">LinkedIn</a>
</div>
```

---

## 기술 요약

| 소스 | 수집 방식 | urllib 가능 | 난이도 |
|:-----|:---------|:----------:|:-----:|
| Anthropic News | __NEXT_DATA__ JSON | ⚠️ | 중 |
| Claude Code Docs | HTML 파싱 | ✅ | 하 |
| Claude API Docs | HTML 파싱 | ✅ | 하 |
| Reddit | JSON API | ✅ 완료 | - |
| YouTube | MCP 도구 | N/A | 하 |
| Instagram | MCP 도구 | N/A | 하 |
| X/Twitter | 불가 | ❌ | - |
| LinkedIn | 불가 | ❌ | - |

---

## 실행 순서 (오토 추천)

1. **즉시**: Anthropic News 수집 함수 구현 + 카테고리 분류 개선
2. **다음**: Claude Code/API Docs 변경 감지
3. **그 다음**: YouTube/Instagram MCP 연동
4. **마지막**: UI 브랜딩 개선

---

*Created by 멘토 (2026-03-27) | 오토 실행 대기*

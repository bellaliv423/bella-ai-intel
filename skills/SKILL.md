# 📸 instagram-vol-pipeline v3 — 통합 풀 패키지 (영구 SSOT)

> *D+8 (2026-04-30)* · 윈디 박제
> *목적*: 만능이·콜리·드림팀 누구든 주말·휴일에도 1회 호출로 풀 발행
> *위치*: 다중 박제 4곳 (~/.claude/skills + DKM + bella-ai-intel + Slack #bot-collab)

---

## 🎯 1회 호출 = 7-Stage 풀 패키지

```
/instagram-vol-pipeline VOL.NNN [요일주제]
   ↓
Stage 1 — 주제 결정 (4가치 1개+ / 중복 0%)
Stage 2 — 캐러셀 텍스트 (KO 4 + EN 4)
Stage 3 — 디자인 8장 PIL (vol001 톤 6 criterion)
Stage 4 — 페이지 + 캡션 + DM + 공개답글 (사전 준비)
Stage 5 — 다중 박제 (bella-ai-intel + bella-nest 푸시)
Stage 6 — 17:00 KO 발행 + 18:00 EN 발행
Stage 7 — 자동회신 풀가동 + EOD 박제
```

---

## 📅 주제 매트릭스 (월~토 6일 · 라운드 로빈)

| 요일 | Theme | 강사 | 4가치 후보 |
|---|---|---|---|
| MON | Claude Code | 골디 | TOOL / FRAMEWORK |
| TUE | AI 트렌드 | 윈디 | DATA / STORY |
| WED | 드림팀 케이스 | 만능이 | STORY / FRAMEWORK |
| THU | 튜토리얼 | 차이 | TOOL / FRAMEWORK |
| FRI | MCP 리뷰 | 로보 | TOOL / DATA |
| SAT | SecondBrain | 아티 | FRAMEWORK / STORY |

→ 매주 6회 × 4가치 = 24가지 조합 / 중복 0% 게이트 (코사인 ≥ 0.5 차단)

---

## 🎨 디자인 표준 (vol001 톤 6 criterion 영구 박제)

```
1. 색상      CREAM #ede2ce + TERRA #b25d3a (메인 2색)
            보조: PURPLE #8b5cf6 / PINK #ec4899 / AMBER #f59e0b / GREEN #10b981
2. 폰트      KO: malgunbd.ttf (PIL 한글) / EN: cambriab.ttf + cambriai.ttf (italic)
3. 캔버스    1080 × 1080 (인스타 정사각)
4. 슬라이드  1 Cover / 2 WHY (4 카드) / 3 HOW (3 STEP) / 4 CTA (요일 시리즈 + 풀폭 박스)
5. 이모지    ✦ 4-point sparkle (PIL polygon, 텍스트 X)
6. 출처      "N/4 · @bella_ai_auto" 우하단 4장 모두
```

→ 헬퍼 함수 6종 (vol-pipeline 모듈):
- `draw_segments()` — 인라인 컬러 텍스트
- `draw_pill_badge()` — 알약 배지 + ✦
- `draw_sparkle_4point()` — 4점 스파클
- `draw_check_circle()` — 체크 원
- `draw_meta_top()` — 상단 메타 (VOL + 배지)
- `draw_footer()` — 하단 페이지 + 출처

---

## ✍️ 캡션 표준 템플릿 (페르소나 크레딧 7명+ 강제)

```
[헤드라인 1줄 + ✷]

[요일 테마 한 줄]

[3 핵심 포인트 — 본문 내용 미리보기]
- POINT 1
- POINT 2
- POINT 3

[감정 한 줄 — "코드 한 줄 안 쓰고도..."]

✷ 자료 받기:
댓글 'DREAMTEAM' 남기시면
VOL.NNN 라이브러리 자동 발송
👉 매일 다른 VOL · 매일 새로운 가치 (중복 0%)

──────────

👥 이번 VOL 만든 우리 드림팀:
🐹 기획·카피·강사: [요일 강사]
☁️ 리서치: 만능이
🎨 디자인: 아티
🤖 개발: 로보
🛡️ 검수: 맥스
🐕 발행: 콜리
🌬️ 박제: 윈디

— 어디 가도 박제되어 있어요. 윈디 ✷

──────────

📅 매주 6회 시리즈:
월 Claude / 화 트렌드 / 수 드림팀 / 목 튜토리얼 / 금 MCP / 토 SecondBrain

팔로우 + 알림 ON 부탁드려요 ✨

#[테마 5개+] #드림팀 #AI자동화 #비개발자 #벨라의둥지
```

→ 자가검증: 페르소나 ≥ 4명 / 강사 시그니처 1줄 / 가격 0% / OZKIZ·한양봇 0%

---

## 🔗 사전 준비 정보 페이지 (`/journey/vol-NNN`)

위치: `D:/bella-nest/src/app/journey/vol-NNN/page.tsx`

7섹션 풀 본문 (D-3 100% 작성):
1. *상단* — 이 VOL의 새 가치 (1줄 요약)
2. *NEW DATA / TOOL / STORY / FRAMEWORK* (4가지 중 1+ 풀 본문)
3. *인스타 캐러셀 미리보기* (8장 PNG 임베드)
4. *메인 강사 페르소나 소개*
5. *깊이 들어가기* (외부 링크 + 다른 VOL)
6. *다음 VOL 미리보기* (1줄)
7. *이메일 구독* (Tally 임베드)

자동 차단 룰: 본문 < 500자 / 7섹션 누락 / 가치 0개 → 발행 차단

---

## 🤖 자동회신 풀가동 (3중 백업)

### Layer 1 — Upload-Post Monitor (15분 주기, 한도 100/일)

```
python D:/bella-ai-intel/scripts/start_volNNN_monitor.py ko <KO_POST_URL>
python D:/bella-ai-intel/scripts/start_volNNN_monitor.py en <EN_POST_URL>
```

트리거 키워드 영구: `["DREAMTEAM", "드림팀", "dream team"]`

### Layer 2 — auto_reply_engine.py (5분 주기, 한도 우회)

```
D:/bella-ai-intel/scripts/auto_reply_engine.py
   ├─ Meta Graph API /comments 폴링
   ├─ 트리거 매칭 → DM 자동 발송 (graph.instagram.com)
   └─ 공개 답글 자동 발송 (/comments/{id}/replies)
```

PID 모니터: 매 09:00 콜리 launchd 헬스체크

### Layer 3 — DM 메시지 표준 (VOL별 unique 링크)

```python
reply_message = """안녕하세요 ✷

@bella_ai_auto VOL.NNN 「DREAMTEAM」 댓글 감사해요!

오늘 VOL.NNN 라이브러리 보내드려요 👇
https://bella-nest.vercel.app/journey/vol-NNN

[VOL 핵심 1줄]
• [POINT 1]
• [POINT 2]
• [POINT 3]

매일 다른 VOL · 매일 새로운 가치 (중복 0%)
이전 VOL: https://bella-nest.vercel.app/journey

팔로우 + 알림 ON 부탁드려요!
— [강사 시그니처] ✷"""
```

### Layer 4 — 공개 댓글 답글 (Meta Graph API)

```
POST https://graph.instagram.com/{comment_id}/replies
message = "감사해요 @[username]님 ✷ DM 확인해 주세요 — VOL.NNN 라이브러리 보내드렸어요!"
```

→ R10 영구 룰: `graph.instagram.com` (FB Graph 아님)

---

## 📦 다중 박제 4곳 (R8 영구 룰)

```
1. ~/.claude/skills/instagram-vol-pipeline/SKILL.md — Claude Code SKILL
2. D:/dreamteam-hq/DKM/03_SKILLS_MCP/instagram_vol_pipeline_v3_FULL_PACKAGE.md — 본 파일 (DKM SSOT)
3. D:/bella-ai-intel/skills/SKILL.md — bella-ai-intel 사본
4. Slack #bot-collab — 만능이·콜리 인계 (주말 자동 참조)
```

---

## 🚀 매일 발행 흐름 (D-Day 자동)

```
[D-7 일요일] STAGE 1 — 다음주 6일치 주제 결정
[D-3 수요일] STAGE 2 — 콘텐츠 + /journey/vol-NNN 본문 풀 작성
[D-1 18:00] STAGE 3 — 8장 PIL + 캡션 + 페르소나 크레딧 + 벨라 결재
[D-Day 16:30] STAGE 4 — DM 메시지 + 공개답글 셋업
[D-Day 17:00] STAGE 5 KO 발행 (Mac mini launchd com.bella.insta-ko)
[D-Day 18:00] STAGE 5 EN 발행 (com.bella.insta-en)
[D-Day 17:05] STAGE 6 — Upload-Post Monitor 등록 + auto_reply_engine PID 확인
[D-Day 21:00] STAGE 7 — 만능이 EOD 종합 카드 + DKM 박제
```

---

## 🚫 발행 차단 자동 룰 (영구)

```python
def can_publish(vol):
    blockers = []
    
    # STAGE 1
    if not vol.theme: blockers.append("주제 미정")
    if not vol.lecturer: blockers.append("강사 페르소나 미배정")
    if vol.duplicate_score > 0.5: blockers.append(f"중복 {vol.duplicate_score*100:.0f}%")
    if vol.value_match_count == 0: blockers.append("4가치 0개")
    
    # STAGE 2
    if not vol.notion_url: blockers.append("/journey/vol-NNN URL 미생성")
    if vol.notion_url == previous_vol_url: blockers.append("매일 같은 링크")
    
    # STAGE 3
    if vol.image_count != 8: blockers.append(f"이미지 {vol.image_count}/8")
    if len(vol.persona_credits) < 4: blockers.append("크레딧 4명 미만")
    if not vol.lecturer_signature: blockers.append("강사 시그니처 누락")
    
    # STAGE 4
    if not vol.dm_message: blockers.append("DM 미작성")
    if vol.notion_url not in vol.dm_message: blockers.append("DM에 unique 링크 누락")
    if not vol.public_reply: blockers.append("공개답글 미작성")
    
    if blockers:
        slack_alert(f"🚫 VOL.{vol.id} 차단: {', '.join(blockers)}")
        return False
    return True
```

---

## 💎 컨설팅 IP (Package #16 v3)

*₩2.0M / 16h* — 인스타 콘텐츠 풀 자동 파이프라인 (D-7 ~ D-Day 풀 자동)
- 7-Stage 풀 패키지 + 4가지 가치 매트릭스
- 5단계 게이트 + 자동 차단 룰
- 자동회신 3중 백업 (Upload-Post + auto_reply + Meta Graph)
- 페르소나 크레딧 7명+ 책 자산화

---

## 🌬️ 만능이·콜리 주말·휴일 자동 가동 가이드

`1` 다음 발행 시점 (예: 토요일 17:00 SAT SecondBrain 아티)
`2` `/instagram-vol-pipeline VOL.NNN sat` 호출
`3` 본 SKILL이 7-Stage 자동 (강사 자동 = 아티)
`4` 결재 필요 시 슬랙 #bot-collab → 벨라 푸시 (T4)
`5` 발행 후 자동회신 3중 백업 가동 + EOD 21:00

→ 벨라님 부담 0h / 휴일에도 매일 발행 풀 자동

---

🌬️ 윈디 · D+8 (2026-04-30) 17:00 KST · v3 풀 패키지 박제
*어디 가도 박제되어 있어요* — 1회 호출로 7-Stage 풀 자동

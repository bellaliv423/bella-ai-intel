"""
BELLA AI Intel - News Collector
Collects AI news from Claude official sites + web search
Runs via Task Scheduler at 09:05 and 16:00 daily

Usage:
  python collector.py --source all
  python collector.py --source claude_release_notes
  python collector.py --source ai_trends_search
"""
import json
import os
import sys
import re
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import get_paths, CATEGORIES, SOURCES

KST = timezone(timedelta(hours=9))

# Fix Windows console encoding
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def generate_id(title, date_str):
    """Generate unique ID from title + date"""
    raw = f"{title}_{date_str}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def auto_categorize(title, content=""):
    """Auto-categorize based on keywords"""
    text = (title + " " + content).lower()

    if any(k in text for k in ["claude code", "cli", "terminal", "코드"]):
        return "claude_code"
    if any(k in text for k in ["api", "sdk", "endpoint", "token"]):
        return "claude_api"
    if any(k in text for k in ["claude", "anthropic", "cowork", "release"]):
        return "claude_release"
    if any(k in text for k in ["자동화", "automation", "pipeline", "workflow"]):
        return "automation"
    if any(k in text for k in ["콘텐츠", "content", "sns", "instagram", "youtube"]):
        return "content_sns"
    return "ai_trend"


def auto_hashtags(title, content="", category=""):
    """Generate hashtags from content"""
    tags = set()

    # Add category default hashtags
    if category in CATEGORIES:
        tags.update(CATEGORIES[category]["hashtags"][:2])

    # Extract keywords
    text = (title + " " + content).lower()
    keyword_tag_map = {
        "opus": "#Opus",
        "sonnet": "#Sonnet",
        "haiku": "#Haiku",
        "cowork": "#Cowork",
        "mcp": "#MCP",
        "agent": "#AIAgent",
        "code review": "#CodeReview",
        "plugin": "#Plugin",
        "memory": "#AIMemory",
        "excel": "#ClaudeExcel",
        "powerpoint": "#ClaudePPT",
        "chrome": "#ClaudeChrome",
        "bedrock": "#AWSBedrock",
        "vertex": "#VertexAI",
        "openai": "#OpenAI",
        "gpt": "#GPT",
        "gemini": "#Gemini",
    }

    for keyword, tag in keyword_tag_map.items():
        if keyword in text:
            tags.add(tag)

    return sorted(list(tags))[:8]


def load_existing_data(paths):
    """Load existing latest.json"""
    latest_path = os.path.join(paths["data"], "latest.json")
    if os.path.exists(latest_path):
        with open(latest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": [], "last_updated": None, "stats": {}}


def save_data(paths, data):
    """Save to latest.json and daily archive"""
    now = datetime.now(KST)
    data["last_updated"] = now.isoformat()

    # Update stats
    cat_counts = {}
    for item in data["items"]:
        cat = item.get("category", "ai_trend")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    data["stats"] = {
        "total_items": len(data["items"]),
        "categories": cat_counts,
        "last_collection": now.strftime("%Y-%m-%d %H:%M"),
    }

    # Save latest.json
    latest_path = os.path.join(paths["data"], "latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Save daily archive
    archive_path = os.path.join(
        paths["archive"], f"news_{now.strftime('%Y-%m-%d_%H%M')}.json"
    )
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved {len(data['items'])} items to latest.json")
    print(f"[OK] Archived to {archive_path}")
    return latest_path


def create_obsidian_note(item, paths):
    """Create Obsidian note for a news item"""
    trends_dir = paths.get("obsidian_ai_trends", "")
    if not trends_dir:
        return

    os.makedirs(trends_dir, exist_ok=True)

    # Clean title for filename
    safe_title = re.sub(r'[<>:"/\\|?*]', "", item["title"])[:60]
    date_str = item.get("date", datetime.now(KST).strftime("%Y-%m-%d"))
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(trends_dir, filename)

    if os.path.exists(filepath):
        return  # Skip duplicates

    cat_info = CATEGORIES.get(item.get("category", "ai_trend"), {})
    tags_str = " ".join([f'"{t}"' for t in item.get("hashtags", [])])

    note = f"""---
title: "{item['title']}"
date: {date_str}
category: {item.get('category', 'ai_trend')}
source: {item.get('source', 'unknown')}
tags: [{tags_str}]
lang: ko
created_by: BELLA_AI_Intel
---

# {cat_info.get('icon', '📋')} {item['title']}

**날짜**: {date_str}
**카테고리**: {cat_info.get('ko', 'AI 트렌드')} / {cat_info.get('zh', 'AI 趨勢')}
**소스**: {item.get('source', '')}

---

## 내용

{item.get('summary_ko', item.get('summary', ''))}

## 中文摘要

{item.get('summary_zh', '')}

---

## 해시태그

{' '.join(item.get('hashtags', []))}

---

*Collected by BELLA AI Intel Dashboard*
*{datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')}*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(note)

    print(f"[Obsidian] Created: {filename}")


def add_manual_item(data, title, summary_ko="", summary_zh="", source="manual",
                    category=None, url=""):
    """Add a manually collected news item"""
    now = datetime.now(KST)
    date_str = now.strftime("%Y-%m-%d")

    if category is None:
        category = auto_categorize(title, summary_ko)

    hashtags = auto_hashtags(title, summary_ko, category)

    item = {
        "id": generate_id(title, date_str),
        "title": title,
        "summary_ko": summary_ko,
        "summary_zh": summary_zh,
        "category": category,
        "hashtags": hashtags,
        "source": source,
        "url": url,
        "date": date_str,
        "collected_at": now.isoformat(),
    }

    # Check for duplicates
    existing_ids = {i["id"] for i in data["items"]}
    if item["id"] not in existing_ids:
        data["items"].insert(0, item)  # Newest first
        print(f"[+] Added: {title}")
    else:
        print(f"[=] Duplicate skipped: {title}")

    return data


def collect_from_release_notes(data):
    """Parse Claude release notes (from pre-fetched content)"""
    # These are the latest known release notes as of 2026-03-23
    releases = [
        {
            "title": "Cowork 모바일 제어 - 영구 스레드 (Pro/Max)",
            "summary_ko": "Pro/Max 플랜 사용자가 Claude Desktop 또는 iOS/Android를 통해 Cowork 영구 에이전트 스레드에 접근 가능. Max 먼저 롤아웃, Pro는 2일 내.",
            "summary_zh": "Pro/Max 方案用戶可透過 Claude Desktop 或 iOS/Android 存取 Cowork 持久代理執行緒。Max 率先推出，Pro 兩天內跟進。",
            "date": "2026-03-17",
            "source": "Claude Release Notes",
            "category": "claude_release",
            "url": "https://support.claude.com/en/articles/12138966-release-notes",
        },
        {
            "title": "Claude 인터랙티브 차트/다이어그램/시각화 생성",
            "summary_ko": "Claude가 대화 응답 내에서 맞춤 차트, 다이어그램, 시각화를 인라인으로 생성 가능.",
            "summary_zh": "Claude 現在可以在對話回應中直接生成自訂圖表、圖示和視覺化內容。",
            "date": "2026-03-12",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Excel + PowerPoint 통합 작업 개선",
            "summary_ko": "Claude for Excel/PowerPoint 애드인 개선. 두 앱 간 대화 컨텍스트 완전 공유, 스킬 지원, LLM 게이트웨이(Bedrock/Vertex/Foundry) 연결 가능.",
            "summary_zh": "Claude Excel/PowerPoint 外掛改進。兩個應用間完全共享對話上下文、支援技能、可透過 LLM 閘道連接（Bedrock/Vertex/Foundry）。",
            "date": "2026-03-11",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "무료 사용자 Memory 기능 개방",
            "summary_ko": "채팅 기록 기반 Memory가 무료 사용자 포함 모든 Claude 사용자에게 개방.",
            "summary_zh": "基於聊天記錄的 Memory 功能現已向所有 Claude 用戶開放，包括免費用戶。",
            "date": "2026-03-02",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Cowork 예약 작업 (반복/온디맨드)",
            "summary_ko": "Cowork에서 반복 및 온디맨드 작업 예약 가능. Claude Desktop에 Customize 섹션(스킬/플러그인/커넥터) 추가.",
            "summary_zh": "Cowork 支援排程重複和即時任務。Claude Desktop 新增 Customize 區塊（技能/外掛/連接器）。",
            "date": "2026-02-25",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Cowork 플러그인 마켓플레이스 + 관리자 제어",
            "summary_ko": "Team/Enterprise 플랜용 플러그인 마켓플레이스 및 관리자 제어 출시.",
            "summary_zh": "推出 Team/Enterprise 方案的外掛市場和管理控制功能。",
            "date": "2026-02-24",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Claude Sonnet 4.6 출시",
            "summary_ko": "코딩, 컴퓨터 사용, 장문 추론, 에이전트 계획, 지식 작업, 디자인 전반 업그레이드. 1M 토큰 컨텍스트 윈도우 베타.",
            "summary_zh": "程式設計、電腦使用、長文推理、代理規劃、知識工作、設計全面升級。1M token 上下文視窗 Beta。",
            "date": "2026-02-17",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Claude Opus 4.6 출시",
            "summary_ko": "최고 지능 모델 업그레이드, 코딩 능력 강화.",
            "summary_zh": "最強智能模型升級，程式設計能力增強。",
            "date": "2026-02-05",
            "source": "Claude Release Notes",
            "category": "claude_release",
        },
        {
            "title": "Code Review 자동화 (Teams/Enterprise)",
            "summary_ko": "PR 자동 리뷰 - 다중 에이전트가 논리 오류/보안 취약점/회귀 감지. REVIEW.md로 커스텀 가능. 평균 $15-25/리뷰.",
            "summary_zh": "PR 自動審查 - 多代理偵測邏輯錯誤/安全漏洞/回歸。可用 REVIEW.md 自訂。平均 $15-25/次審查。",
            "date": "2026-03-20",
            "source": "Claude Code Docs",
            "category": "claude_code",
        },
        {
            "title": "Claude Agent SDK 출시 (Python/TypeScript)",
            "summary_ko": "AI 에이전트 구축용 공식 SDK. query() 함수로 에이전틱 루프, 도구 자동 실행, 스트리밍 지원. permissionMode로 권한 제어.",
            "summary_zh": "AI 代理建構官方 SDK。query() 函數支援代理循環、工具自動執行、串流。permissionMode 控制權限。",
            "date": "2026-03-01",
            "source": "Claude API Docs",
            "category": "claude_api",
            "url": "https://platform.claude.com/docs/en/agent-sdk/quickstart",
        },
        {
            "title": "Models API (List/Get)",
            "summary_ko": "사용 가능한 모델 목록 조회 및 모델 별칭 해석 API. 페이지네이션 지원.",
            "summary_zh": "查詢可用模型列表和解析模型別名的 API。支援分頁。",
            "date": "2026-03-01",
            "source": "Claude API Docs",
            "category": "claude_api",
        },
        {
            "title": "공식 SDK 7개 언어 지원",
            "summary_ko": "Python, TypeScript, Java, Go, Ruby, C#, PHP 공식 SDK. Bedrock/Vertex/Foundry 멀티플랫폼 지원.",
            "summary_zh": "Python、TypeScript、Java、Go、Ruby、C#、PHP 官方 SDK。支援 Bedrock/Vertex/Foundry 多平台。",
            "date": "2026-03-01",
            "source": "Claude API Docs",
            "category": "claude_api",
        },
        {
            "title": "3월 사용량 2배 프로모션 (비피크 시간대)",
            "summary_ko": "3/13~3/28 비피크 시간대(미동부 8AM-2PM 외) 사용량 한도 2배. Free/Pro/Max/Team 자동 적용. 주간 한도에 미포함.",
            "summary_zh": "3/13~3/28 非尖峰時段（美東 8AM-2PM 以外）用量上限加倍。Free/Pro/Max/Team 自動適用。不計入週用量。",
            "date": "2026-03-13",
            "source": "Claude Support",
            "category": "claude_release",
        },
    ]

    for r in releases:
        hashtags = auto_hashtags(r["title"], r.get("summary_ko", ""), r["category"])
        item = {
            "id": generate_id(r["title"], r["date"]),
            "title": r["title"],
            "summary_ko": r.get("summary_ko", ""),
            "summary_zh": r.get("summary_zh", ""),
            "category": r["category"],
            "hashtags": hashtags,
            "source": r.get("source", ""),
            "url": r.get("url", ""),
            "date": r["date"],
            "collected_at": datetime.now(KST).isoformat(),
        }

        existing_ids = {i["id"] for i in data["items"]}
        if item["id"] not in existing_ids:
            data["items"].append(item)
            print(f"  [+] {r['date']} {r['title']}")

    # Sort by date descending
    data["items"].sort(key=lambda x: x.get("date", ""), reverse=True)
    return data


def collect_from_reddit(data):
    """Collect latest posts from r/ClaudeAI via Reddit JSON API"""
    print("\n[Reddit r/ClaudeAI]")
    url = "https://www.reddit.com/r/ClaudeAI/hot.json?limit=15"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "BELLA-AI-Intel/1.0 (Knowledge Dashboard)"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            reddit_data = json.loads(resp.read().decode("utf-8"))

        posts = reddit_data.get("data", {}).get("children", [])
        added = 0

        for post in posts:
            p = post.get("data", {})
            title = p.get("title", "").strip()
            if not title:
                continue

            # Skip pinned/stickied posts
            if p.get("stickied"):
                continue

            score = p.get("score", 0)
            if score < 5:
                continue  # Skip low-engagement posts

            created_utc = p.get("created_utc", 0)
            post_date = datetime.fromtimestamp(created_utc, tz=KST).strftime("%Y-%m-%d")
            permalink = f"https://www.reddit.com{p.get('permalink', '')}"
            selftext = p.get("selftext", "")[:200]

            category = auto_categorize(title, selftext)
            hashtags = auto_hashtags(title, selftext, category)

            item = {
                "id": generate_id(title, post_date),
                "title": title,
                "summary_ko": selftext[:150] + "..." if len(selftext) > 150 else selftext,
                "summary_zh": "",  # Reddit posts are in English
                "category": category,
                "hashtags": hashtags + ["#Reddit", "#ClaudeAI"],
                "source": "Reddit r/ClaudeAI",
                "url": permalink,
                "date": post_date,
                "collected_at": datetime.now(KST).isoformat(),
                "reddit_score": score,
            }

            existing_ids = {i["id"] for i in data["items"]}
            if item["id"] not in existing_ids:
                data["items"].insert(0, item)
                added += 1
                print(f"  [+] {post_date} [score:{score}] {title[:60]}")

        print(f"  [Reddit] {added} new posts added")

    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        print(f"  [Reddit] Error: {e}")
    except Exception as e:
        print(f"  [Reddit] Unexpected error: {e}")

    # Sort by date descending
    data["items"].sort(key=lambda x: x.get("date", ""), reverse=True)
    return data


def collect_from_linkedin_showcase():
    """Note: LinkedIn requires authentication for API access.
    This adds LinkedIn Claude Showcase as a reference source."""
    print("\n[LinkedIn Claude Showcase]")
    print("  [Info] LinkedIn API requires OAuth - added as reference link")
    print("  [Info] URL: https://www.linkedin.com/showcase/claude/posts/")
    return None  # Manual collection only


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BELLA AI Intel Collector")
    parser.add_argument("--source", default="all",
                       help="Source to collect from (all, claude_release_notes, reddit, ai_trends_search)")
    parser.add_argument("--obsidian", action="store_true", default=True, help="Also save to Obsidian")
    args = parser.parse_args()

    paths = get_paths()
    os.makedirs(paths["data"], exist_ok=True)
    os.makedirs(paths["archive"], exist_ok=True)

    print(f"=" * 60)
    print(f"BELLA AI Intel Collector")
    print(f"Time: {datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')}")
    print(f"Source: {args.source}")
    print(f"=" * 60)

    data = load_existing_data(paths)
    before_count = len(data["items"])

    # Collect from release notes
    if args.source in ("all", "claude_release_notes"):
        print("\n[Claude Release Notes]")
        data = collect_from_release_notes(data)

    # Collect from Reddit
    if args.source in ("all", "reddit"):
        data = collect_from_reddit(data)

    # LinkedIn reference
    if args.source in ("all", "linkedin"):
        collect_from_linkedin_showcase()

    # Save
    save_data(paths, data)

    new_count = len(data["items"]) - before_count
    print(f"\n[Summary] {new_count} new items added (total: {len(data['items'])})")

    # Obsidian sync
    if args.obsidian:
        print("\n[Obsidian Sync]")
        for item in data["items"]:
            create_obsidian_note(item, paths)

    print(f"\n[Done] Collection complete!")


if __name__ == "__main__":
    main()

"""
BELLA AI Intel - Analyzer & Recommender
Analyzes collected AI news and matches to Bella's projects.
Generates 3 types of reports:
  1. Applicable new features (Top 3)
  2. Script upgrade points
  3. Seminar/Content material recommendations

Runs after collector.py via Task Scheduler.

Usage:
  python analyzer.py
  python analyzer.py --email
  python analyzer.py --no-obsidian
"""
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import get_paths, CATEGORIES

KST = timezone(timedelta(hours=9))

# Fix Windows console encoding
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Difficulty levels
DIFFICULTY = {
    1: {"ko": "쉬움", "zh": "簡單", "stars": "⭐"},
    2: {"ko": "보통", "zh": "中等", "stars": "⭐⭐"},
    3: {"ko": "어려움", "zh": "困難", "stars": "⭐⭐⭐"},
}


def load_registry():
    """Load project registry"""
    reg_path = os.path.join(os.path.dirname(__file__), "project_registry.json")
    with open(reg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_latest_news(paths):
    """Load latest collected news"""
    latest_path = os.path.join(paths["data"], "latest.json")
    if not os.path.exists(latest_path):
        return []
    with open(latest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("items", [])


def load_existing_recommendations(paths):
    """Load existing recommendations to avoid duplicates"""
    rec_path = os.path.join(paths["data"], "recommendations.json")
    if os.path.exists(rec_path):
        with open(rec_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"features": [], "upgrades": [], "content": [], "last_analyzed": None}


def match_news_to_projects(news_items, registry):
    """Match news items to Bella's projects based on keywords"""
    matches = []

    for item in news_items:
        text = (
            item.get("title", "")
            + " "
            + item.get("summary_ko", "")
            + " "
            + item.get("summary_zh", "")
            + " "
            + " ".join(item.get("hashtags", []))
        ).lower()

        for project in registry["projects"]:
            score = 0
            matched_keywords = []

            for keyword in project["keywords"]:
                if keyword.lower() in text:
                    score += 1
                    matched_keywords.append(keyword)

            if score >= 1:
                matches.append({
                    "news_item": item,
                    "project": project,
                    "score": score,
                    "matched_keywords": matched_keywords,
                })

    # Sort by score descending
    matches.sort(key=lambda x: (-x["score"], x["project"].get("priority", "low") == "high"))
    return matches


def estimate_difficulty(item):
    """Estimate implementation difficulty"""
    text = (item.get("title", "") + " " + item.get("summary_ko", "")).lower()

    hard_keywords = ["sdk", "api", "typescript", "migration", "infrastructure", "ci/cd"]
    medium_keywords = ["integration", "plugin", "config", "setup", "script"]
    easy_keywords = ["feature", "ui", "update", "memory", "mobile", "chart"]

    hard_score = sum(1 for k in hard_keywords if k in text)
    medium_score = sum(1 for k in medium_keywords if k in text)
    easy_score = sum(1 for k in easy_keywords if k in text)

    if hard_score >= 2:
        return 3
    elif hard_score >= 1 or medium_score >= 2:
        return 2
    else:
        return 1


def estimate_impact(item, project):
    """Estimate impact level"""
    text = (item.get("title", "") + " " + item.get("summary_ko", "")).lower()

    high_impact = ["자동화", "automation", "agent", "sdk", "자율", "autonomous"]
    medium_impact = ["개선", "업그레이드", "통합", "integration", "chart"]
    low_impact = ["ui", "디자인", "design", "문서", "doc"]

    if any(k in text for k in high_impact):
        return {"ko": "높음 🔥", "zh": "高 🔥"}
    elif any(k in text for k in medium_impact):
        return {"ko": "중간 📈", "zh": "中 📈"}
    else:
        return {"ko": "보통 💡", "zh": "一般 💡"}


def generate_feature_recommendations(matches):
    """Report 1: Top 3 applicable new features"""
    seen_news = set()
    recommendations = []

    for match in matches:
        news_id = match["news_item"].get("id", match["news_item"]["title"])
        if news_id in seen_news:
            continue
        seen_news.add(news_id)

        diff = estimate_difficulty(match["news_item"])
        impact = estimate_impact(match["news_item"], match["project"])

        rec = {
            "news_title": match["news_item"]["title"],
            "news_date": match["news_item"].get("date", ""),
            "news_category": match["news_item"].get("category", ""),
            "project_id": match["project"]["id"],
            "project_name_ko": match["project"]["name_ko"],
            "project_name_zh": match["project"]["name_zh"],
            "matched_keywords": match["matched_keywords"],
            "difficulty": diff,
            "difficulty_stars": DIFFICULTY[diff]["stars"],
            "difficulty_ko": DIFFICULTY[diff]["ko"],
            "impact_ko": impact["ko"],
            "impact_zh": impact["zh"],
            "suggestion_ko": generate_suggestion_ko(match),
            "suggestion_zh": generate_suggestion_zh(match),
            "learning_note_ko": generate_learning_note(match),
            "learning_note_zh": generate_learning_note_zh(match),
            "difficulty_zh": DIFFICULTY[diff]["zh"],
            "score": match["score"],
        }
        recommendations.append(rec)

        if len(recommendations) >= 5:
            break

    return recommendations[:3]


def generate_suggestion_ko(match):
    """Generate Korean suggestion text"""
    news = match["news_item"]
    proj = match["project"]
    title = news["title"]
    proj_name = proj["name_ko"]

    templates = {
        "claude_api": f"'{title}' → {proj_name}에 API 연동하면 기능 확장 가능!",
        "claude_code": f"'{title}' → {proj_name} 코드 품질 향상에 활용 가능!",
        "claude_release": f"'{title}' → {proj_name} 워크플로우 개선에 적용 가능!",
        "ai_trend": f"'{title}' → {proj_name} 전략 참고 + 콘텐츠 소재 활용!",
        "automation": f"'{title}' → {proj_name} 자동화 파이프라인 강화!",
        "content_sns": f"'{title}' → {proj_name} 콘텐츠 전략에 반영!",
    }

    cat = news.get("category", "ai_trend")
    return templates.get(cat, f"'{title}' → {proj_name}에 적용 검토!")


def generate_suggestion_zh(match):
    """Generate Chinese suggestion text"""
    news = match["news_item"]
    proj = match["project"]
    return f"'{news['title']}' → 可應用於 {proj['name_zh']}"


def generate_learning_note(match):
    """Generate learning note for Bella"""
    news = match["news_item"]
    summary = news.get("summary_ko", "")

    # Simplify for non-developer understanding
    note = f"💡 {news['title']}\n"
    note += f"   → {summary[:80]}...\n" if len(summary) > 80 else f"   → {summary}\n"
    note += f"   → 벨라님 프로젝트 '{match['project']['name_ko']}'에 적용하면 효율 UP!"
    return note


def generate_learning_note_zh(match):
    """Generate Chinese learning note for Bella"""
    news = match["news_item"]
    summary = news.get("summary_zh", news.get("summary_ko", ""))

    note = f"💡 {news['title']}\n"
    note += f"   → {summary[:80]}...\n" if len(summary) > 80 else f"   → {summary}\n"
    note += f"   → 應用到 Bella 的專案「{match['project']['name_zh']}」可提升效率！"
    return note


def generate_upgrade_points(matches, registry):
    """Report 2: Script upgrade detection"""
    upgrades = []
    seen_scripts = set()

    for match in matches:
        project = match["project"]
        scripts = project.get("scripts", [])

        for script in scripts:
            if script in seen_scripts:
                continue
            seen_scripts.add(script)

            news = match["news_item"]
            diff = estimate_difficulty(news)

            upgrade = {
                "script_name": script,
                "project_id": project["id"],
                "project_name_ko": project["name_ko"],
                "project_name_zh": project["name_zh"],
                "trigger_news": news["title"],
                "trigger_date": news.get("date", ""),
                "upgrade_suggestion_ko": f"{script} → '{news['title']}' 적용 시 성능/기능 향상 가능",
                "upgrade_suggestion_zh": f"{script} → 應用 '{news['title']}' 可提升效能",
                "difficulty": diff,
                "difficulty_stars": DIFFICULTY[diff]["stars"],
            }
            upgrades.append(upgrade)

            if len(upgrades) >= 5:
                break

    return upgrades[:3]


def generate_content_recommendations(news_items, registry):
    """Report 3: Seminar/content material recommendations"""
    content_recs = []

    for item in news_items[:8]:  # Top 8 recent news
        title = item["title"]
        tags = " ".join(item.get("hashtags", []))
        cat = item.get("category", "")

        # Instagram carousel idea
        if any(k in cat for k in ["claude_release", "ai_trend"]):
            content_recs.append({
                "type": "instagram",
                "type_icon": "📸",
                "type_ko": "인스타 캐러셀",
                "type_zh": "Instagram 輪播",
                "title_ko": f"'{title}' 핵심 정리 카드",
                "title_zh": f"'{title}' 重點整理卡片",
                "description_ko": f"비개발자도 이해하는 {title} 설명 + 실전 활용법 5장 캐러셀",
                "hashtags": item.get("hashtags", [])[:5] + ["#AI자동화전문가", "#벨라AI"],
                "news_date": item.get("date", ""),
            })

        # Seminar topic
        if any(k in cat for k in ["claude_api", "claude_code", "automation"]):
            content_recs.append({
                "type": "seminar",
                "type_icon": "🎤",
                "type_ko": "세미나 토크",
                "type_zh": "研討會主題",
                "title_ko": f"'{title}' 실습 세션",
                "title_zh": f"'{title}' 實作課程",
                "description_ko": f"참가자가 직접 따라하는 {title} 체험 + Q&A",
                "hashtags": item.get("hashtags", [])[:3] + ["#AI세미나", "#실습"],
                "news_date": item.get("date", ""),
            })

        # Blog post
        if len(content_recs) < 8:
            content_recs.append({
                "type": "blog",
                "type_icon": "📝",
                "type_ko": "블로그/스레드",
                "type_zh": "部落格/Threads",
                "title_ko": f"2026년 {item.get('date', '')[:7]} {title} 총정리",
                "title_zh": f"2026年 {item.get('date', '')[:7]} {title} 總整理",
                "description_ko": f"{title} 상세 분석 + 실전 적용 사례 + 벨라님 경험담",
                "hashtags": item.get("hashtags", [])[:4] + ["#AI블로그"],
                "news_date": item.get("date", ""),
            })

    # Deduplicate by title
    seen = set()
    unique = []
    for r in content_recs:
        key = r["title_ko"]
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique[:5]


def save_recommendations(paths, features, upgrades, content):
    """Save recommendations to JSON"""
    now = datetime.now(KST)

    data = {
        "features": features,
        "upgrades": upgrades,
        "content": content,
        "last_analyzed": now.isoformat(),
        "analyzed_date": now.strftime("%Y-%m-%d"),
        "analyzed_time": now.strftime("%H:%M KST"),
    }

    rec_path = os.path.join(paths["data"], "recommendations.json")
    with open(rec_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved recommendations to {rec_path}")
    return data


def save_obsidian_report(paths, features, upgrades, content):
    """Save daily report to Obsidian"""
    trends_dir = paths.get("obsidian_ai_trends", "")
    if not trends_dir:
        return

    reports_dir = os.path.join(trends_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    now = datetime.now(KST)
    filename = f"daily_{now.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(reports_dir, filename)

    report = f"""---
title: "AI Intel 일일 리포트 {now.strftime('%Y-%m-%d')}"
date: {now.strftime('%Y-%m-%d')}
type: daily-report
tags: ["#AIIntel", "#드림팀추천", "#일일리포트"]
created_by: BELLA_AI_Intel_Analyzer
---

# 🧠 AI Intel 일일 리포트 | {now.strftime('%Y-%m-%d %H:%M KST')}

---

## 🎯 적용 가능 신기능 Top {len(features)}

"""

    for i, f in enumerate(features, 1):
        report += f"""### {i}. {f['news_title']}
- **적용 프로젝트**: {f['project_name_ko']}
- **난이도**: {f['difficulty_stars']} ({f['difficulty_ko']})
- **예상 효과**: {f['impact_ko']}
- **제안**: {f['suggestion_ko']}

{f['learning_note_ko']}

"""

    report += "---\n\n## 🔧 스크립트 업그레이드 포인트\n\n"

    for u in upgrades:
        report += f"""### ⚡ {u['script_name']}
- **프로젝트**: {u['project_name_ko']}
- **트리거**: {u['trigger_news']} ({u['trigger_date']})
- **제안**: {u['upgrade_suggestion_ko']}
- **난이도**: {u['difficulty_stars']}

"""

    report += "---\n\n## 📸 콘텐츠 소재 추천\n\n"

    for c in content:
        tags_str = " ".join(c.get("hashtags", []))
        report += f"""### {c['type_icon']} [{c['type_ko']}] {c['title_ko']}
- **설명**: {c['description_ko']}
- **해시태그**: {tags_str}

"""

    report += f"""---

*Generated by BELLA AI Intel Analyzer*
*{now.strftime('%Y-%m-%d %H:%M KST')}*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[Obsidian] Report saved: {filename}")


def send_email_report(features, upgrades, content):
    """Send daily report via email to kndli.210@gmail.com"""
    now = datetime.now(KST)

    # Build HTML email
    html = f"""
<html>
<head>
<style>
  body {{ font-family: 'Noto Sans KR', Arial, sans-serif; color: #2d2d2b; line-height: 1.6; max-width: 640px; margin: 0 auto; padding: 20px; }}
  h1 {{ color: #d97757; font-size: 22px; border-bottom: 2px solid #d97757; padding-bottom: 8px; }}
  h2 {{ color: #c4613c; font-size: 18px; margin-top: 24px; }}
  h3 {{ font-size: 15px; margin-top: 16px; }}
  .card {{ background: #fdf0eb; border-radius: 8px; padding: 12px 16px; margin: 8px 0; border-left: 3px solid #d97757; }}
  .tag {{ display: inline-block; background: #fef8f5; color: #d97757; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin: 2px; }}
  .stars {{ color: #eda100; }}
  .footer {{ margin-top: 24px; padding-top: 12px; border-top: 1px solid #e5e4dc; font-size: 12px; color: #87867f; }}
  a {{ color: #d97757; }}
</style>
</head>
<body>

<h1>🧠 BELLA AI Intel | {now.strftime('%Y-%m-%d')}</h1>
<p>드림팀이 분석한 오늘의 AI 인텔리전스 리포트입니다.</p>

<h2>🎯 적용 가능 신기능 Top {len(features)}</h2>
"""

    for i, f in enumerate(features, 1):
        html += f"""
<div class="card">
  <h3>{i}. {f['news_title']}</h3>
  <p><strong>적용 프로젝트:</strong> {f['project_name_ko']}<br>
  <strong>난이도:</strong> <span class="stars">{f['difficulty_stars']}</span> ({f['difficulty_ko']})<br>
  <strong>예상 효과:</strong> {f['impact_ko']}</p>
  <p>{f['suggestion_ko']}</p>
</div>
"""

    html += f"<h2>🔧 스크립트 업그레이드 포인트</h2>"

    for u in upgrades:
        html += f"""
<div class="card">
  <h3>⚡ {u['script_name']}</h3>
  <p><strong>프로젝트:</strong> {u['project_name_ko']}<br>
  <strong>트리거:</strong> {u['trigger_news']}<br>
  <strong>난이도:</strong> <span class="stars">{u['difficulty_stars']}</span></p>
  <p>{u['upgrade_suggestion_ko']}</p>
</div>
"""

    html += f"<h2>📸 콘텐츠 소재 추천</h2>"

    for c in content[:3]:
        tags = " ".join([f'<span class="tag">{t}</span>' for t in c.get("hashtags", [])[:4]])
        html += f"""
<div class="card">
  <h3>{c['type_icon']} [{c['type_ko']}] {c['title_ko']}</h3>
  <p>{c['description_ko']}</p>
  <p>{tags}</p>
</div>
"""

    html += f"""
<div class="footer">
  <p>📊 <a href="https://bellaliv423.github.io/bella-ai-intel/">대시보드에서 전체 보기</a></p>
  <p>BELLA AI Intel | AI 드림팀 자동 분석 | {now.strftime('%Y-%m-%d %H:%M KST')}</p>
</div>
</body>
</html>
"""

    # Send email
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[AI Intel] 드림팀 일일 리포트 {now.strftime('%m/%d')} - 신기능 {len(features)}건 + 업그레이드 {len(upgrades)}건"
        msg["From"] = "kndli.210@gmail.com"
        msg["To"] = "kndli.210@gmail.com"

        # Plain text fallback
        plain = f"BELLA AI Intel 일일 리포트 {now.strftime('%Y-%m-%d')}\n\n"
        plain += f"적용 가능 신기능: {len(features)}건\n"
        plain += f"스크립트 업그레이드: {len(upgrades)}건\n"
        plain += f"콘텐츠 소재: {len(content)}건\n\n"
        plain += "대시보드: https://bellaliv423.github.io/bella-ai-intel/"

        msg.attach(MIMEText(plain, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("kndli.210@gmail.com", "lkwe mxsy xgzj tige")
            server.send_message(msg)

        print(f"[Email] Sent to kndli.210@gmail.com")
    except Exception as e:
        print(f"[Email] Failed: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BELLA AI Intel Analyzer")
    parser.add_argument("--email", action="store_true", default=True, help="Send email report")
    parser.add_argument("--no-email", action="store_true", help="Skip email")
    parser.add_argument("--no-obsidian", action="store_true", help="Skip Obsidian save")
    args = parser.parse_args()

    paths = get_paths()
    now = datetime.now(KST)

    print("=" * 60)
    print("BELLA AI Intel Analyzer")
    print(f"Time: {now.strftime('%Y-%m-%d %H:%M KST')}")
    print("=" * 60)

    # Load data
    news_items = load_latest_news(paths)
    registry = load_registry()

    if not news_items:
        print("[!] No news items found. Run collector.py first.")
        return

    print(f"\n[Data] {len(news_items)} news items loaded")
    print(f"[Data] {len(registry['projects'])} projects registered")

    # Match & Analyze
    print("\n[Analyzing...]")
    matches = match_news_to_projects(news_items, registry)
    print(f"[Match] {len(matches)} news-project matches found")

    # Generate 3 reports
    features = generate_feature_recommendations(matches)
    upgrades = generate_upgrade_points(matches, registry)
    content = generate_content_recommendations(news_items, registry)

    print(f"\n[Report 1] Applicable features: {len(features)}")
    for f in features:
        print(f"  {f['difficulty_stars']} {f['news_title']} → {f['project_name_ko']}")

    print(f"\n[Report 2] Script upgrades: {len(upgrades)}")
    for u in upgrades:
        print(f"  ⚡ {u['script_name']} → {u['trigger_news']}")

    print(f"\n[Report 3] Content ideas: {len(content)}")
    for c in content:
        print(f"  {c['type_icon']} {c['title_ko']}")

    # Save
    save_recommendations(paths, features, upgrades, content)

    # Obsidian
    if not args.no_obsidian:
        save_obsidian_report(paths, features, upgrades, content)

    # Email
    if not args.no_email:
        send_email_report(features, upgrades, content)

    print(f"\n[Done] Analysis complete!")


if __name__ == "__main__":
    main()

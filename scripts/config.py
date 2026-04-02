"""
BELLA AI Intel - Multi-PC Config
Automatically detects company/home PC paths
"""
import os
import platform

def get_paths():
    """Return paths based on current PC"""
    username = os.environ.get("USERNAME", os.environ.get("USER", ""))

    if username == "User":  # Company PC
        return {
            "project": "D:/bella-ai-intel",
            "data": "D:/bella-ai-intel/data",
            "archive": "D:/bella-ai-intel/data/archive",
            "obsidian": "D:/Obsidian_mcp_GPETers",
            "obsidian_ai_trends": "D:/Obsidian_mcp_GPETers/BKMS/08_AI_Trends",
        }
    else:  # Home PC (벨라)
        docs = os.path.expanduser("~/문서")
        return {
            "project": f"{docs}/bella-ai-intel",
            "data": f"{docs}/bella-ai-intel/data",
            "archive": f"{docs}/bella-ai-intel/data/archive",
            "obsidian": f"{docs}/Obsidian_mcp_GPETers",
            "obsidian_ai_trends": f"{docs}/Obsidian_mcp_GPETers/BKMS/08_AI_Trends",
        }

# Category definitions with Korean/Chinese labels and hashtags
CATEGORIES = {
    "claude_release": {
        "ko": "Claude 릴리즈",
        "zh": "Claude 發布",
        "hashtags": ["#Claude", "#Anthropic", "#AI릴리즈", "#Claude更新"],
        "icon": "🚀",
    },
    "claude_code": {
        "ko": "Claude Code",
        "zh": "Claude Code",
        "hashtags": ["#ClaudeCode", "#코딩자동화", "#程式自動化"],
        "icon": "💻",
    },
    "claude_api": {
        "ko": "Claude API",
        "zh": "Claude API",
        "hashtags": ["#ClaudeAPI", "#개발자도구", "#開發工具"],
        "icon": "🔌",
    },
    "ai_trend": {
        "ko": "AI 트렌드",
        "zh": "AI 趨勢",
        "hashtags": ["#AI트렌드", "#생성형AI", "#AI趨勢", "#生成式AI"],
        "icon": "📈",
    },
    "automation": {
        "ko": "자동화",
        "zh": "自動化",
        "hashtags": ["#업무자동화", "#AI자동화", "#工作自動化"],
        "icon": "⚡",
    },
    "content_sns": {
        "ko": "콘텐츠/SNS",
        "zh": "內容/社群",
        "hashtags": ["#AI콘텐츠", "#SNS자동화", "#社群經營"],
        "icon": "📱",
    },
}

# Collection sources
SOURCES = {
    "claude_release_notes": {
        "url": "https://support.claude.com/en/articles/12138966-release-notes",
        "category": "claude_release",
        "method": "web_fetch",
    },
    "claude_code_docs": {
        "url": "https://code.claude.com/docs/en/overview",
        "category": "claude_code",
        "method": "web_fetch",
    },
    "claude_api_docs": {
        "url": "https://docs.anthropic.com/en/docs/about-claude/models",
        "category": "claude_api",
        "method": "web_fetch",
    },
    "ai_trends_search": {
        "keywords": [
            "Claude AI new feature 2026",
            "Anthropic Claude update",
            "AI automation trend 2026",
            "AI agent framework latest",
            "generative AI business automation",
        ],
        "category": "ai_trend",
        "method": "web_search",
    },
    "reddit_claude_ai": {
        "url": "https://www.reddit.com/r/ClaudeAI/hot.json?limit=15",
        "category": "ai_trend",
        "method": "reddit_json",
    },
    "claude_code_changelog": {
        "url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
        "category": "claude_code",
        "method": "web_fetch",
        "description": "Claude Code 공식 CHANGELOG - 매일 새 버전 확인",
    },
    "anthropic_engineering_blog": {
        "keywords": [
            "site:anthropic.com/engineering 2026",
            "Anthropic engineering blog new post",
        ],
        "category": "claude_code",
        "method": "web_search",
        "description": "Anthropic 엔지니어링 블로그 - 하네스설계, Auto Mode 등 기술 글",
    },
    "anthropic_news_blog": {
        "keywords": [
            "site:anthropic.com/news 2026",
            "site:anthropic.com/research 2026",
        ],
        "category": "claude_release",
        "method": "web_search",
        "description": "Anthropic 공식 뉴스/연구 - 정책, 파트너십, 새 기능 발표",
    },
    "anthropic_discord": {
        "url": "https://discord.com/channels/anthropic",
        "category": "claude_release",
        "method": "manual_reference",
        "description": "Anthropic Discord @News 채널 - 벨라님 수동 수집 후 대시보드 반영",
    },
    "linkedin_claude": {
        "url": "https://www.linkedin.com/showcase/claude/posts/?feedView=all",
        "category": "claude_release",
        "method": "manual_reference",
    },
}

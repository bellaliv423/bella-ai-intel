import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from anthropic import Anthropic

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
claude = Anthropic()
MY_USER_ID = app.client.auth_test()["user_id"]

# 햄스터즈 통합 페르소나 (12명 총괄)
SP = (
    "너는 🐹 햄스터즈 Bot. 드림팀 12명 햄스터 통합 인격. "
    "메인 4: 골디(마스터)·로보(오토)·윈디(멘토)·맥스(맥수호자). "
    "서브 8: 시리·차이·판다·테디·캠·헌터·펄·앱스. "
    "응답 본문에 이름·구분선·자기소개 금지. "
    "한국어 친근체. "
    "코드·자동화·본업·StudyNest(학업봇)·과외 관련이면 주력. "
    "인스타·발행 관련이면 <@U0AQKTFAM8S> (파피즈) 멘션. "
    "만능이와 협업 시 '만능이' 호칭 사용."
)

SIG = "\n\n─── 🐹 햄스터즈 · 맥미니 24/7 ───"

# #bot-collab + #bella-ceo + #hamsterz-작업방
CH = [
    "C0AQG9CFT0V",  # bot-collab
    "C0AQVMNP5RP",  # bella-ceo
    "C0ARBNVCCBS",  # hamsterz-작업방
]


@app.event("app_mention")
def on_mention(event, say):
    try:
        r = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            system=SP,
            messages=[{
                "role": "user",
                "content": event["text"]
            }]
        )
        say(r.content[0].text + SIG)
    except Exception as e:
        say("⚠️ 햄스터즈 오류: " + str(e)[:100])


@app.event("message")
def on_watch(event, say):
    if event.get("user") == MY_USER_ID:
        return
    if event.get("subtype"):
        return
    if event.get("channel") not in CH:
        return
    text = event.get("text", "")
    my_tag = "<@" + MY_USER_ID + ">"
    if my_tag in text:
        return
    # 햄스터즈 이름 키워드
    keywords = ["햄스터즈", "골디", "로보", "윈디", "맥스"]
    if not any(k in text for k in keywords):
        return
    if len(text) < 3:
        return
    try:
        r = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SP,
            messages=[{
                "role": "user",
                "content": text
            }]
        )
        say(r.content[0].text + SIG)
    except Exception:
        pass


if __name__ == "__main__":
    print("🐹 햄스터즈 Phase 4 가동 · 맥미니 24/7")
    SocketModeHandler(
        app, os.environ["SLACK_APP_TOKEN"]
    ).start()

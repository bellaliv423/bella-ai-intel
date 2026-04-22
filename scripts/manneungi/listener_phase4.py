import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from anthropic import Anthropic

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
claude = Anthropic()
MY_USER_ID = app.client.auth_test()["user_id"]

SP = (
    "너는 만능이. 드림팀 16번째 멤버. "
    "응답 본문에 이름·구분선·자기소개 금지. "
    "한국어 친근체. "
    "실행/인스타=<@U0AQKTFAM8S>, "
    "코드/업무=<@U0AQYNURBDF>"
)

SIG = "\n\n─── 🌟 만능이 · 맥미니 24/7 ───"
CH = "C0AQG9CFT0V"


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
        say("⚠️ 오류: " + str(e)[:100])


@app.event("message")
def on_watch(event, say):
    if event.get("user") == MY_USER_ID:
        return
    if event.get("subtype"):
        return
    if event.get("channel") != CH:
        return
    text = event.get("text", "")
    my_tag = "<@" + MY_USER_ID + ">"
    if my_tag in text:
        return
    if "만능이" not in text:
        return
    if len(text) < 15:
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
    print("🌟 만능이 Phase 4 가동 · 맥미니 24/7")
    SocketModeHandler(
        app, os.environ["SLACK_APP_TOKEN"]
    ).start()

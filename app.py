from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 환경변수에서 봇 토큰과 채팅 ID 가져오기
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# 루트 테스트용
@app.route("/", methods=["GET"])
def home():
    return "✅ 서버가 잘 실행되고 있어요!", 200

# 웹훅 엔드포인트
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method != "POST":
        return "GET not allowed", 405

    data = request.get_json()
    message = data.get("message", "📭 메시지가 없습니다")

    try:
        response = requests.post(TELEGRAM_URL, data={
            "chat_id": CHAT_ID,
            "text": message
        })
        print(f"✅ 전송 코드: {response.status_code}")
        print(f"📬 응답 내용: {response.text}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    return "OK", 200

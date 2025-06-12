from flask import Flask, request
import os
import requests

app = Flask(__name__)

# 환경변수에서 봇 토큰과 챗 ID 가져오기
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# 웹훅 엔드포인트 설정
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method != "POST":
        return "GET not allowed", 405

    data = request.get_json()
    message = data.get("message", "[알림] 메시지가 없습니다")

    print(f"📥 수신한 메시지: {message}")
    print(f"📦 전체 수신 데이터: {data}")

    try:
        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })
        print(f"✅ 텔레그램 전송 코드: {response.status_code}")
        print(f"✅ 텔레그램 전송 응답: {response.text}")
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")

    return "OK", 200

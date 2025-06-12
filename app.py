from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 환경변수에서 토큰과 챗 ID 불러오기
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method != "POST":
        return "GET not allowed", 405

    data = request.get_json()
    message = data.get("message", "❗메시지가 없습니다")

    print(f"📨 수신한 메시지: {message}")
    print(f"🧾 전체 데이터: {data}")

    try:
        response = requests.post(TELEGRAM_URL, data={
            "chat_id": CHAT_ID,
            "text": message
        })
        print(f"✅ 응답 코드: {response.status_code}")
        print(f"✅ 응답 내용: {response.text}")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

    return "OK", 200

# Render 환경일 때는 gunicorn이 실행함
if __name__ == "__main__":
    print("🧪 개발 환경에서 직접 실행 중 (Render에선 무시됨)")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    print("🚀 Render 배포 성공: 서버가 gunicorn으로 실행되고 있습니다.")

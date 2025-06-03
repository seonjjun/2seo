import os
import requests
from flask import Flask

app = Flask(__name__)

# 환경변수에서 값 불러오기 (Render의 Environment 탭 기준)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/send", methods=["GET"])
def send_message():
    message = "✅ 성공이다! Render 서버에서 드디어 메시지 보낸다!!! 🥳✏️"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=data)
    return "✅ 메시지 전송 완료!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

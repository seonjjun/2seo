import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = "8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI"
CHAT_ID = "7541910616"  # 성준이의 chat_id

@app.route("/send")  # ← 이 줄이 없으면 /send 접근 안 됨!
def send_message():
    message = "성준아! Render 서버에서 드디어 메시지 보낸다!!! 🎯"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)
    return "메시지 전송 완료!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

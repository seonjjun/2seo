import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = "8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI"
CHAT_ID = "7541910616"  # 성준이의 실제 chat_id 숫자

@app.route("/send")
def send_message():
    message = "성준아! Render 서버에서 보내는 메시지야 🎯"
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

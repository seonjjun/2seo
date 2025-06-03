import requests
from flask import Flask

app = Flask(__name__)

# 🔥 환경변수 대신 직접 입력
TELEGRAM_TOKEN = "8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI"
CHAT_ID = "7541916016"

@app.route("/send")
def send_message():
    message = "이서가 보내는 첫 번째 메시지 😎"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)
    return "메시지 전송 완료!"

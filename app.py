import os
import requests
from flask import Flask
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

app = Flask(__name__)

# 환경변수에서 토큰과 챗아이디 불러오기
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

import requests
from flask import Flask, request

app = Flask(__name__)

# 🌐 성준이의 텔레그램 봇 정보
TELEGRAM_TOKEN = "8170134694:AAFD3DbDd-2ZhhDHYy-H1KAwxW_AXyzjqsQ"
CHAT_ID = "7541916016"

@app.route('/')
def home():
    return "2seo Alert Bot is running!"

@app.route('/send')
def send_message():
    # URL에 전달된 메시지를 가져오기 (예: /send?text=안녕)
    message = request.args.get('text', '기본 메시지입니다 😊')

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)
    return f"📤 보낸 결과: {response.json()}"


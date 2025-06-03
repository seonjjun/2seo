from flask import Flask
import requests

app = Flask(__name__)

# 성준이의 텔레그램 정보
TELEGRAM_TOKEN = "8170134694:AAFD3DbDd-2ZhhDHYy-H1KAwxW_AXyzjqsQ"
CHAT_ID = "7541916016"

@app.route('/')
def home():
    return "2seo Alert Bot is running!"

@app.route('/send')
def send_message():
    message = "이서가 보내는 첫 번째 메시지야 😎"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    return f"보낸 결과: {response.json()}"

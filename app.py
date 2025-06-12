from flask import Flask, request
import os
import requests

app = Flask(__name__)

# 텔레그램 봇 토큰과 챗 ID
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# 웹훅 엔드포인트
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method != "POST":
        return "GET not allowed", 405

    data = request.get_json()
    message = data.get("message", "💬 기본 메시지입니다.")

    try:
        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })
        print(f"✅ 텔레그램 전송 완료: {response.status_code}")
        print(f"📨 응답: {response.text}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    return "OK", 200

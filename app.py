from flask import Flask, request
import os
import requests

app = Flask(__name__)

# 환경변수에서 텔레그램 토큰과 채팅 ID 가져오기
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method != "POST":
        return "GET not allowed", 405

    data = request.get_json()
    message = data.get("message", "[경고] 메시지가 없습니다")

    try:
        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })
        print(f"✅ 전송 완료 - 코드: {response.status_code}")
        print(f"📨 응답: {response.text}")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

    return "OK", 200

if __name__ == '__main__':
    app.run()

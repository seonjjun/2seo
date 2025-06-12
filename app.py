from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 환경변수에서 불러오기
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message', '📡 데이터 수신: ' + str(data))

    try:
        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })
        print(f"✅ 텔레그램 응답 코드: {response.status_code}")
        print(f"📨 응답 내용: {response.text}")
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")

    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

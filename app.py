from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 텔레그램 정보
BOT_TOKEN = '8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI'
CHAT_ID = '7541916016'
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
    port = int(os.environ.get("PORT", 5000))  # Render용 포트 설정
    app.run(host='0.0.0.0', port=port)

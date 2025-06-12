from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 환경변수에서 토큰과 채팅 ID 불러오기
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# 웹훅 엔드포인트
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print(f"📩 수신된 데이터: {data}")

        message = data.get('message', '메시지가 없습니다.')
        print(f"📤 전송할 메시지: {message}")

        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })

        print(f"✅ 상태 코드: {response.status_code}")
        print(f"✅ 응답 내용: {response.text}")

        return "OK", 200

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return "Error", 500

# 실행 시작
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render가 지정한 포트 사용
    app.run(host='0.0.0.0', port=port)

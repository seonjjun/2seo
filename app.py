from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ 요청 로깅 (웹훅 테스트 확인용)
@app.before_request
def log_request_info():
    print(f"📡 요청 도착: {request.method} {request.path}")

# ✅ 환경변수에서 텔레그램 정보 불러오기
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# ✅ 웹훅 경로
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        print("⚠️ GET 요청은 무시됩니다.")
        return 'GET Not Allowed', 405

    # POST 요청일 때
    data = request.get_json()
    message = data.get('message', '[경고] 메시지가 없습니다')

    print(f"✅ 받은 메시지: {message}")
    print(f"📦 전체 데이터: {data}")

    try:
        response = requests.post(TELEGRAM_URL, data={
            'chat_id': CHAT_ID,
            'text': message
        })
        print(f"📤 텔레그램 응답코드: {response.status_code}")
        print(f"📨 응답 본문: {response.text}")
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")

    return 'OK', 200

# ✅ 서버 실행
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

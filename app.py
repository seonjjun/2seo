from flask import Flask, request
import os, requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message', '[none]')
    print("📨 메시지:", message)
    try:
        res = requests.post(f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
                             data={'chat_id': os.environ['CHAT_ID'], 'text': message})
        print("✅ 텔레그램 응답:", res.text)
    except Exception as e:
        print("❌ 전송 에러:", e)
    return 'OK', 200

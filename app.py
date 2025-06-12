from flask import Flask, request
import requests

app = Flask(__name__)

# === 텔레그램 설정 ===
TELEGRAM_TOKEN = '8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI'
CHAT_ID = '7541916016'  # ← 숫자 그대로!

# === 이서 분석기 함수 ===
def analyze_alert(data):
    symbol = data.get('symbol', 'Unknown')
    interval = data.get('interval', 'N/A')
    price = data.get('price', 'N/A')
    condition = data.get('condition', '')
    tag = data.get('strategy_tag', 'UNKNOWN')
    note = data.get('note', '')

    # 전략 해석
    if tag == 'LONG_ENTRY_SIGNAL' and 'RSI' in condition:
        return f"📈 *롱 진입 시그널*\n심볼: {symbol}\n주기: {interval}\n현재가: {price}\n조건: `{condition}`\n📝 {note}"
    elif tag == 'SHORT_BREAKDOWN' and 'EMA' in condition:
        return f"📉 *숏 붕괴 시그널*\n심볼: {symbol}\n주기: {interval}\n현재가: {price}\n조건: `{condition}`\n📝 {note}"
    else:
        return f"⚠️ *미분석 알림 도착*\n데이터: {data}"

# === 텔레그램 전송 함수 ===
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# === 웹훅 엔드포인트 ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return {'status': 'no data received'}, 400

    # 이서 분석기 작동
    message = analyze_alert(data)

    # 텔레그램 전송
    send_telegram_message(message)

    return {'status': 'alert processed'}, 200

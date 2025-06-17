from flask import Flask, request, jsonify
import requests
import weaviate
import os
import hmac
import base64
import hashlib
import time
from datetime import datetime, timezone  # 🔥 타임스탬프 오류 방지용

app = Flask(__name__)

# === 텔레그램 설정 ===
TELEGRAM_TOKEN = '8170134694:AAF9WM10B9A9LvmfAPe26WoRse1oMUGwECI'
CHAT_ID = '7541916016'  # ← 숫자 그대로!

# === Weaviate 설정 ===
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY),
)

# === 벡터 추출 함수 ===
def extract_feature_vector(data):
    return [data.get("rsi", 0), data.get("obv", 0), data.get("volume", 0)]

# === 분석 API (/analyze) ===
@app.route('/analyze', methods=['POST'])
def analyze_structure():
    try:
        incoming = request.get_json()
        features = extract_feature_vector(incoming)

        response = client.query.get("Structure", [
            "id", "description", "success", "time", "image"
        ])\
        .with_near_vector({"vector": features})\
        .with_limit(3)\
        .do()

        results = response['data']['Get']['Structure']
        return jsonify({"status": "ok", "results": results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/store', methods=['POST'])
def store_structure():
    try:
        structure = request.get_json()
        if not structure:
            return jsonify({"status": "error", "message": "No data received"}), 400

        client.data_object.create(
            structure,
            class_name="Structure",
            uuid=structure.get("id")  # 선택사항: 생략하면 자동 생성됨
        )

        return jsonify({"status": "ok", "message": f"Stored {structure.get('id')}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# === 삭제 API (/delete-structure) ===
@app.route('/delete-structure', methods=['POST'])
def delete_structure():
    try:
        data = request.get_json()
        uuid = data.get("uuid")
        if not uuid:
            return jsonify({"status": "error", "message": "UUID is required"}), 400

        client.data_object.delete(uuid=uuid, class_name="Structure")
        return jsonify({"status": "ok", "message": f"Deleted {uuid}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# === 이서 분석기 함수 (웹훅 알림용) ===
def analyze_alert(data):
    symbol = data.get('symbol', 'Unknown')
    interval = data.get('interval', 'N/A')
    price = data.get('price', 'N/A')
    condition = data.get('condition', '')
    tag = data.get('strategy_tag', 'UNKNOWN')
    note = data.get('note', '')

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

# === 웹훅 알림 엔드포인트 (/webhook) ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return {'status': 'no data received'}, 400

    message = analyze_alert(data)
    send_telegram_message(message)
    return {'status': 'alert processed'}, 200

# === OKX 잔고 확인 API (/test-okx-balance) ===
API_KEY = 'ff8d0b4a-fdda-4de1-a579-b2076593b7fa'
SECRET_KEY = '49E886BC5608EAB889274AB16323A1B1'
PASSPHRASE = '#eseoAI0612'

def generate_signature(timestamp, method, request_path, body):
    message = f'{timestamp}{method}{request_path}{body}'
    mac = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

def get_balances():
    url = 'https://www.okx.com/api/v5/account/balance'
    timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
    method = 'GET'
    request_path = '/api/v5/account/balance'
    body = ''

    headers = {
        'OK-ACCESS-KEY': API_KEY,
        'OK-ACCESS-SIGN': generate_signature(timestamp, method, request_path, body),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except Exception as e:
        return {
            "error": "❌ OKX 응답 파싱 실패",
            "status_code": response.status_code,
            "text": response.text,
            "exception": str(e)
        }

@app.route('/test-okx-balance', methods=['GET'])
def test_okx_balance():
    return get_balances()

from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
import json

app = Flask(__name__)

# Delta Exchange API Credentials
API_KEY = "your_api_key_here"
API_SECRET = "your_secret_key_here"
BASE_URL = "https://api.delta.exchange"  # Delta Exchange API Base URL

# Function to place an order on Delta Exchange
def place_order(side, quantity, symbol):
    endpoint = "/v2/orders"
    url = BASE_URL + endpoint
    
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    order_data = {
        "product_id": 24,  # BTC Perpetual (Check Product ID from Delta API)
        "size": quantity,
        "side": side,  # "buy" or "sell"
        "order_type": "market",
        "leverage": 10  # Change leverage as needed
    }
    
    # Create HMAC Signature
    signature = hmac.new(API_SECRET.encode(), json.dumps(order_data).encode(), hashlib.sha256).hexdigest()
    headers["api-signature"] = signature
    
    response = requests.post(url, headers=headers, json=order_data)
    return response.json()
code
# Webhook Endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    alert_message = data.get("message", "")
    
    if "BUY" in alert_message:
        response = place_order("buy", 0.009, "BTCUSD")  # Adjust quantity
    elif "SELL" in alert_message:
        response = place_order("sell", 0.009, "BTCUSD")
    else:
        return jsonify({"error": "Unknown alert type"}), 400
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

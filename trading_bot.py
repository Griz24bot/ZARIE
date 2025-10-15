from flask import Flask, request, jsonify
import os
from telegram import Bot
import requests
from MINER_BOT import zarie, dashboard, vault

app = Flask(__name__)

class TradingViewWebhookBot:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "7575096974:AAGn1yVwkaNbsNFYHkz6cvPq6crAWkMaoeE")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id_here")
        self.telegram_bot = Bot(token=self.bot_token)

    def send_trade_signal(self, signal):
        """Route trade signals to secure Telegram channel"""
        try:
            message = f"🛡️ TradingView Signal: {signal}"
            self.telegram_bot.send_message(chat_id=self.chat_id, text=message)

            # Also send via requests for reliability
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message}
            requests.post(url, data=payload)

            print(f"TradingView signal sent: {signal}")
        except Exception as e:
            print(f"Failed to send trade signal: {e}")

    def process_signal(self, data):
        """Process incoming TradingView webhook signal"""
        try:
            # Extract signal data
            strategy = data.get("strategy", {})
            ticker = data.get("ticker", "UNKNOWN")
            order_action = strategy.get("order_action", "none")
            price = data.get("price", 0)
            time = data.get("time", "unknown")

            # Create signal message
            signal = f"{order_action.upper()} {ticker} at ${price} (Time: {time})"

            # Send to Telegram
            self.send_trade_signal(signal)

            # Trigger ZARIE and dashboard animations
            zarie.speak(f"TradingView signal received: {signal}. Sovereign ritual initiated.")
            dashboard.animate("glyph_signal_pulse", target="vault_seal")

            # Log to vault
            vault.log_to_vault("TradingView Signal", {
                "signal": signal,
                "ticker": ticker,
                "action": order_action,
                "price": price,
                "timestamp": time
            })

            # Trigger override vote for trades
            if order_action in ["buy", "sell"]:
                dashboard.trigger_override("Z-18")
                zarie.speak(f"Heirs summoned for {order_action} override on {ticker}.")

            return {"status": "success", "message": "Signal processed"}

        except Exception as e:
            error_msg = f"Error processing signal: {str(e)}"
            print(error_msg)
            return {"status": "error", "message": error_msg}

# Global webhook bot instance
webhook_bot = TradingViewWebhookBot()

@app.route('/tradingview-webhook', methods=['POST'])
def tradingview_webhook():
    """Receive TradingView webhook signals"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        print(f"Received TradingView webhook: {data}")

        # Process the signal
        result = webhook_bot.process_signal(data)

        return jsonify(result), 200 if result["status"] == "success" else 500

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "tradingview-webhook-bot"}), 200

def run_webhook_server():
    """Run the Flask webhook server"""
    print("Starting TradingView Webhook Bot...")
    print("Webhook URL: http://localhost:5000/tradingview-webhook")
    print("Health Check: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=False)

# Example TradingView alert payload structure:
"""
{
  "ticker": "BTCUSDT",
  "price": 45000,
  "time": "2023-10-15T10:30:00Z",
  "strategy": {
    "order_action": "buy",
    "order_contracts": 1,
    "order_price": 45000,
    "order_id": "123456",
    "market_position": "long",
    "market_position_size": 1
  }
}
"""

if __name__ == "__main__":
    run_webhook_server()

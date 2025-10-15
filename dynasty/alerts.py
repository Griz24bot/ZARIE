import logging
from telegram import Bot

# Telegram configuration (replace with your actual tokens)
TELEGRAM_TOKEN = "8279538827:AAGJhkXSgF-6k94ni_O1k643rfm2Z2tkOVk"
CHAT_ID = "YOUR_CHAT_ID"
bot = Bot(token=TELEGRAM_TOKEN)

async def send_alert(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

# Specific alert functions
def alert_dns_failure(error, agent_name):
    send_alert(f"⚠️ DNS Failure for {agent_name}: {error}. Agent may be offline.")

def alert_mutation_triggered(agent_name, mutation):
    send_alert(f"🧬 Mutation proposed for {agent_name}: {mutation}")

def alert_repair_success(agent_name):
    send_alert(f"✅ {agent_name} repaired successfully.")

def alert_repair_failure(agent_name, error):
    send_alert(f"⚠️ {agent_name} repair failed: {error}")

def alert_telegram(message):
    send_alert(message)

import asyncio
import logging
from dotenv import load_dotenv
import os

load_dotenv()

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import TradingAgent, RobinhoodAdapter, AlpacaAdapter, VaultLogger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from robin_credentials import ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD
from memory import BotMemory
from orchestrator import Orchestrator
from assets import CryptoAssetRegistry
from dashboard import TradingDashboard
from arbitrage import ArbitrageScanner
from on_zarie import OnZARIE, WELCOME_MESSAGE
from telegram_bot import TelegramBot, AgentManager

logging.basicConfig(level=logging.INFO)

#####################
# CONFIGURATION
#####################
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL')
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_PRIVATE_KEY = os.getenv('COINBASE_PRIVATE_KEY')

#####################
# SIMULATE OUTAGE
#####################
async def simulate_outage(agent):
    await asyncio.sleep(5)
    logging.warning(f"[{agent.name}] Simulating platform outage.")
    # Fix: Ensure second is within 0-59 range
    current_second = agent.last_heartbeat.second
    new_second = max(0, current_second - 30)
    agent.last_heartbeat = agent.last_heartbeat.replace(second=new_second)

#####################
# MAIN ASYNC LOOP
#####################
async def main():
    memory = BotMemory()

    # Initialize asset registry
    asset_registry = CryptoAssetRegistry()
    asset_registry.fetch_all()

    # Get platform-specific assets
    alpaca_assets = asset_registry.get_platform_assets("Alpaca")
    robinhood_assets = asset_registry.get_platform_assets("Robinhood")

    # Create adapters
    robinhood_adapter = RobinhoodAdapter(ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD)
    alpaca_adapter = AlpacaAdapter(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

    # Create arbitrage scanner
    adapters = {"Alpaca": alpaca_adapter, "Robinhood": robinhood_adapter}
    arbitrage_scanner = ArbitrageScanner(adapters)

    # Create agents with asset lists
    agents = [
        TradingAgent("AlpacaAgent", alpaca_adapter, memory, alpaca_assets),
        TradingAgent("RobinhoodAgent", robinhood_adapter, memory, robinhood_assets)
    ]

    # Create dashboard
    dashboard = TradingDashboard()
    dashboard.asset_registry = asset_registry

    # Create orchestrator
    orchestrator = Orchestrator({'api_key': COINBASE_API_KEY, 'api_secret': COINBASE_PRIVATE_KEY}, {'api_key': ALPACA_API_KEY, 'api_secret': ALPACA_SECRET_KEY, 'base_url': ALPACA_BASE_URL})

    # Initialize ZARIE
    zarie = OnZARIE(avatar="Alexis", role="Oracle", voice="sovereign", orchestrator=orchestrator, memory=memory)
    zarie.speak(WELCOME_MESSAGE)
    zarie.animate("greeting")

    # Initialize Telegram Bot
    telegram_bot = TelegramBot(zarie, orchestrator)
    asyncio.create_task(telegram_bot.poll_updates())

    # Simulate outage for testing
    asyncio.create_task(simulate_outage(orchestrator.agents[0]))

    # Run arbitrage scanning in background
    async def arbitrage_loop():
        while True:
            common_assets = asset_registry.get_common_assets()
            for asset in common_assets:
                opportunities = arbitrage_scanner.scan(asset)
                for opp in opportunities:
                    arbitrage_scanner.execute_arbitrage(opp)
                    arbitrage_scanner.trigger_mutation_on_spread(opp)
                    dashboard.log_trade_summary("ArbitrageScanner", asset, "arbitrage", opp["spread"])
            await asyncio.sleep(10)  # Scan every 10 seconds

    asyncio.create_task(arbitrage_loop())

    # Display dashboard periodically
    async def dashboard_loop():
        while True:
            dashboard.display_dashboard()
            await asyncio.sleep(30)  # Update every 30 seconds

    asyncio.create_task(dashboard_loop())

    # Run ZARIE voice interface in background
    asyncio.create_task(zarie.run_voice_interface())

    # Run all agents concurrently
    await orchestrator.run()

if __name__ == '__main__':
    asyncio.run(main())

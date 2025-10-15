import asyncio
import logging
from datetime import datetime, timedelta
from agents import TradingAgent, RobinhoodAdapter, AlpacaAdapter
from memory import BotMemory
from alerts import alert_repair_failure

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, coinbase_keys, alpaca_keys):
        self.coinbase_keys = coinbase_keys
        self.alpaca_keys = alpaca_keys
        self.memory = BotMemory()
        self.agents = []
        self.setup_agents()

    def setup_agents(self):
        from robin_credentials import ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD
        robinhood_adapter = RobinhoodAdapter(ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD)
        alpaca_adapter = AlpacaAdapter(self.alpaca_keys['api_key'], self.alpaca_keys['api_secret'], self.alpaca_keys['base_url'])

        self.agents.append(TradingAgent("RobinhoodAgent", robinhood_adapter, self.memory))
        self.agents.append(TradingAgent("AlpacaAgent", alpaca_adapter, self.memory))

    async def run(self):
        while True:
            tasks = [agent.run() for agent in self.agents]
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.monitor_and_repair()
            await asyncio.sleep(10)  # Orchestrate every 10 seconds

    async def monitor_and_repair(self):
        for agent in self.agents:
            if not agent.is_healthy():
                logger.warning(f"[{agent.name}] Unhealthy, attempting repair...")
                try:
                    await agent.repair()
                except Exception as e:
                    alert_repair_failure(agent.name, str(e))
                    if agent.failure_count >= 3:
                        mutation = agent.propose_mutation("execution resilience")
                        from alerts import alert_mutation_triggered
                        alert_mutation_triggered(agent.name, mutation)

    async def simulate_outage(self, agent_name):
        for agent in self.agents:
            if agent.name == agent_name:
                logging.warning(f"[{agent.name}] Simulating full outage.")
                agent.last_heartbeat = datetime.utcnow() - timedelta(seconds=60)
                agent.status = "error"
                break

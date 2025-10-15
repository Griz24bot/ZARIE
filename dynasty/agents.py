import logging
import asyncio
import time
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory import BotMemory
from config import MUTATION_DRAW_DOWN_THRESHOLD, MUTATION_ACCURACY_THRESHOLD
from trading import coinbase_trade, moving_average_crossover

logger = logging.getLogger(__name__)

#####################
# PLATFORM ADAPTERS
#####################
class PlatformAdapter:
    def execute(self, signal):
        pass  # Override in subclasses

class RobinhoodAdapter(PlatformAdapter):
    def __init__(self, username, password):
        import robin_stocks as r
        self.r = r
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self):
        if not self.logged_in:
            try:
                import robin_stocks as r
                r.login(self.username, self.password)
                self.logged_in = True
                print("Robinhood login successful")
            except Exception as e:
                print(f"Robinhood login failed: {e}")
                raise e

    def execute(self, signal):
        self.login()
        import time
        import logging
        for attempt in range(3):
            try:
                if signal['action'].lower() == 'buy':
                    order = self.r.order_buy_market(signal['symbol'], signal.get('qty', 1))
                elif signal['action'].lower() == 'sell':
                    order = self.r.order_sell_market(signal['symbol'], signal.get('qty', 1))
                else:
                    raise ValueError(f"Unsupported action: {signal['action']}")
                VaultLogger.log_trade(f"Robinhood: {signal['action']} {signal.get('qty', 1)} {signal['symbol']}")
                return order
            except Exception as e:
                logging.warning(f"[ROBINHOOD ERROR] Attempt {attempt+1}: {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    raise RuntimeError(f"Failed to execute trade on Robinhood for {signal['symbol']}")

    def get_best_bid_ask(self, symbol):
        # Robinhood doesn't have direct bid/ask, simulate with last price
        try:
            quote = self.r.get_crypto_quote(symbol)
            price = float(quote['mark_price'])
            return {"bid_price": str(price - 0.01), "ask_price": str(price + 0.01)}
        except Exception as e:
            logger.error(f"Failed to get Robinhood quote for {symbol}: {e}")
            return {"bid_price": "0", "ask_price": "0"}

class AlpacaAdapter(PlatformAdapter):
    def __init__(self, api_key, api_secret, base_url):
        from alpaca_trade_api.rest import REST
        self.api = REST(api_key, api_secret, base_url)
        self.base_url = base_url
        self.api_key = api_key
        self.secret_key = api_secret
        self.headers = {"APCA-API-KEY-ID": self.api_key, "APCA-API-SECRET-KEY": self.secret_key}

    def execute(self, signal):
        try:
            # Add retry logic for DNS issues
            import time
            from socket import gaierror
            for attempt in range(3):
                try:
                    order = self.api.submit_order(
                        symbol=signal['symbol'],
                        qty=signal.get('qty', 1),
                        side=signal['action'],
                        type='market',
                        time_in_force='gtc'
                    )
                    VaultLogger.log_trade(f"Alpaca: {signal['action']} {signal.get('qty', 1)} {signal['symbol']}")
                    return order
                except gaierror as dns_e:
                    from alerts import alert_dns_failure
                    alert_dns_failure(str(dns_e), "AlpacaAgent")
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                    else:
                        raise dns_e
                except Exception as inner_e:
                    logging.warning(f"Alpaca fetch failed: {inner_e}")
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                    else:
                        raise inner_e
        except Exception as e:
            VaultLogger.log_trade(f"Alpaca Error: {e}")
            raise e

    def get_best_bid_ask(self, symbol):
        try:
            quote = self.api.get_latest_quote(symbol)
            return {"bid_price": str(quote.bidprice), "ask_price": str(quote.askprice)}
        except Exception as e:
            logger.error(f"Failed to get Alpaca quote for {symbol}: {e}")
            return {"bid_price": "0", "ask_price": "0"}

    def create_account(self, user_data):
        import requests
        url = f"{self.base_url}/v1/accounts"
        response = requests.post(url, json=user_data, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Account creation failed: {response.text}")

    def create_ach_relationship(self, account_id, bank_info):
        import requests
        url = f"{self.base_url}/v1/accounts/{account_id}/ach_relationships"
        response = requests.post(url, json=bank_info, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"ACH relationship creation failed: {response.text}")

    def initiate_ach_transfer(self, account_id, relationship_id, amount):
        import requests
        url = f"{self.base_url}/v1/accounts/{account_id}/transfers"
        payload = {
            "transfer_type": "ach",
            "relationship_id": relationship_id,
            "amount": str(amount),
            "direction": "INCOMING"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"ACH transfer initiation failed: {response.text}")

    def journal_funds(self, from_account, to_account, amount):
        import requests
        url = f"{self.base_url}/v1/journals"
        payload = {
            "entry_type": "JNLC",
            "amount": str(amount),
            "from_account": from_account,
            "to_account": to_account
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Journaling failed: {response.text}")

    def place_order(self, account_id, symbol, qty, side="buy"):
        import requests
        url = f"{self.base_url}/v1/trading/accounts/{account_id}/orders"
        payload = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": "market",
            "time_in_force": "day"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Order placement failed: {response.text}")

    def listen_to_journal_events(self, account_id):
        import requests
        import json
        url = f"{self.base_url}/v1/events/journal/updates"
        with requests.get(url, stream=True, headers=self.headers) as response:
            for line in response.iter_lines():
                if line:
                    event = json.loads(line.decode("utf-8").replace("data: ", ""))
                    self.memory.log("Journal Event", event)  # Assuming memory is accessible

#####################
# TRADING AGENT
#####################
class TradingAgent:
    def __init__(self, name, adapter, memory, asset_list=None):
        self.name = name
        self.adapter = adapter
        self.memory = memory
        self.asset_list = asset_list or ["AAPL"]  # Default fallback
        self.last_heartbeat = datetime.utcnow()
        self.status = "active"
        self.failure_count = 0

    async def run(self):
        while self.status == "active":
            try:
                for asset in self.asset_list:
                    signal = self.generate_signal(asset)
                    if signal:
                        self.adapter.execute(signal)
                        self.memory.log("Signal Executed", {"asset": asset, "signal": signal})
                self.last_heartbeat = datetime.utcnow()
                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                self.status = "error"
                self.memory.log_error(e)
                await self.repair()
                self.failure_count += 1
                if self.failure_count >= 3:
                    mutation = self.propose_mutation("resilience upgrade")
                    from alerts import alert_mutation_triggered
                    alert_mutation_triggered(self.name, mutation)

    def receive_message(self, message):
        print(f"[{self.name}] Received message from ZARIE: {message}")
        # Optional: Process message, e.g., adjust behavior

    def generate_signal(self, asset):
        # Simulate signal generation for specific asset
        import random
        action = random.choice(["buy", "sell"])
        qty = random.randint(1, 5)
        return {"symbol": asset, "action": action, "qty": qty}

    def is_healthy(self):
        return (datetime.utcnow() - self.last_heartbeat) < timedelta(seconds=20)

    async def repair(self):
        logger.info(f"[{self.name}] Attempting self-repair...")
        await asyncio.sleep(3)  # Simulate reconnect
        self.status = "active"
        self.last_heartbeat = datetime.utcnow()
        from alerts import alert_repair_success
        alert_repair_success(self.name)

class BaseAgent:
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory
        self.performance = {"roi": 10.0, "drawdown": 2.0, "accuracy": 0.8}

    def act(self):
        pass  # Override in subclasses

    def generate_signals(self, market_data):
        # Simulate signals
        return [{"symbol": "AAPL", "action": "buy", "risk": "low"}]

    def mutate(self, strategy):
        print(f"[{self.name}] Mutating with strategy: {strategy}")
        # Simulate mutation
        self.performance["roi"] += 1.0

    def get_live_metrics(self):
        return self.performance

    def propose_mutation(self, lineage, metrics):
        if metrics["drawdown"] > MUTATION_DRAW_DOWN_THRESHOLD or metrics["accuracy"] < MUTATION_ACCURACY_THRESHOLD:
            proposal = {
                "agent_id": self.name,
                "proposed_mutation": "risk-adjusted",
                "rationale": f"Performance breach: drawdown {metrics['drawdown']}, accuracy {metrics['accuracy']}",
                "confidence": 0.8,
                "requires_vote": True
            }
            VaultLogger.log_proposal(proposal)
            return proposal
        return None

class TrendSpiderBot(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("TrendSpiderBot", memory)
        self.api = api
        self.sub_agents = [SpiderV2(self.memory, self.api), SpiderGuard(self.memory, self.api)]

    def act(self):
        # Implement chart analysis and trading
        print(f"[{self.name}] Analyzing trends...")
        for sub in self.sub_agents:
            sub.act()

class SpiderV2(BaseAgent):
    def act(self):
        print(f"[{self.name}] Refining trend strategies...")

class SpiderGuard(BaseAgent):
    def act(self):
        print(f"[{self.name}] Guarding against trend reversals...")

class TradeIdeasBot(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("TradeIdeasBot", memory)
        self.api = api
        self.sub_agents = [MomentumX(self.memory, self.api), SignalForge(self.memory, self.api)]

    def act(self):
        print(f"[{self.name}] Generating signals...")
        for sub in self.sub_agents:
            sub.act()

class MomentumX(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("MomentumX", memory)
        self.api = api

    def act(self):
        print(f"[{self.name}] Boosting momentum signals...")

class SignalForge(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("SignalForge", memory)
        self.api = api

    def act(self):
        print(f"[{self.name}] Forging advanced signals...")

class MacroSentinel(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("MacroSentinel", memory)
        self.api = api
        self.sub_agents = [EpochEye(self.memory, self.api), LiquidityScanner(self.memory, self.api)]

    def act(self):
        print(f"[{self.name}] Monitoring macro conditions...")
        for sub in self.sub_agents:
            sub.act()

class EpochEye(BaseAgent):
    def act(self):
        print(f"[{self.name}] Scanning for epoch shifts...")

class LiquidityScanner(BaseAgent):
    def act(self):
        print(f"[{self.name}] Scanning liquidity flows...")

# New Agents
class RiskSentinelV2(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("RiskSentinel-V2", memory)
        self.api = api

    def act(self):
        print(f"[{self.name}] Monitoring volatility and adjusting exposure...")

    def monitor_volatility(self):
        print(f"[{self.name}] Monitoring volatility...")

    def adjust_exposure(self):
        print(f"[{self.name}] Adjusting exposure...")

class SpiderV4(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("SpiderV4", memory)
        self.api = api

    def act(self):
        print(f"[{self.name}] Fusing signals and executing trades...")

    def fuse_signals(self, agents):
        print(f"[{self.name}] Fusing signals from {agents}...")

    def execute_trades(self):
        print(f"[{self.name}] Executing trades...")

# Co-Mutated Agent
class MomentumMacroX(BaseAgent):
    def __init__(self, memory, api):
        super().__init__("MomentumMacroX", memory)
        self.api = api

    def act(self):
        print(f"[{self.name}] Combining momentum signals with macro filters for optimized execution...")

#####################
# STRATEGIC DEBATE (Multi-Agent Voting)
#####################
class StrategicDebate:
    @staticmethod
    def resolve(signals):
        # Simulate voting: if majority agree on high-risk, proceed
        high_risk_signals = [s for s in signals if s.get('risk') == 'high']
        if len(high_risk_signals) > len(signals) / 2:
            return [s for s in signals if s.get('risk') == 'high']  # Proceed with high-risk
        return signals  # All signals

#####################
# VAULT LOGGER
#####################
class VaultLogger:
    @staticmethod
    def log(minute, trades, signals, mutations=None):
        print(f"[VAULT LOG] Minute {minute}: Trades={trades}, Signals={signals}, Mutations={mutations}")

    @staticmethod
    def log_trade(trade):
        print(f"[VAULT LOG] Trade: {trade}")

    @staticmethod
    def log_proposal(proposal):
        print(f"[VAULT LOG] Mutation Proposal: {proposal}")

    @staticmethod
    def log_mutation_triggered(agent_name, perf):
        print(f"[VAULT LOG] Mutation Triggered for {agent_name}: {perf}")

    @staticmethod
    def log_rejection(rejection):
        print(f"[VAULT LOG] Mutation Rejection: {rejection}")

#####################
# MUTATION LEARNER
#####################
class MutationLearner:
    def __init__(self):
        self.rejection_logs = []

    def log_rejection(self, rejection):
        self.rejection_logs.append(rejection)

    def refine_proposal(self, rejection_log):
        if rejection_log["reason"] == "low confidence":
            # Simulate training on successful mutations
            print(f"[LEARNER] Training on successful mutations for {rejection_log['agent_id']}")
            return {"improvement": "Trained on 3x more data, confidence +12%"}
        elif rejection_log["reason"] == "strategic misalignment":
            # Align with epoch goals
            print(f"[LEARNER] Aligning with epoch goals for {rejection_log['agent_id']}")
            return {"improvement": "Aligned with current epoch objectives"}
        return {"improvement": "General refinement"}

#####################
# CO-MUTATION ENGINE
#####################
class CoMutationEngine:
    def __init__(self, registry):
        self.registry = registry

    def find_partner(self, agent):
        candidates = [a for a in self.registry if self.is_complementary(agent, a)]
        if candidates:
            return max(candidates, key=lambda a: self.synergy_score(agent, a))
        return None

    def is_complementary(self, agent1, agent2):
        # Simulate complementarity: different types or shared lineage
        return agent1 != agent2 and (agent1 in ["MomentumX", "MacroSentinel"] or agent2 in ["MomentumX", "MacroSentinel"])

    def synergy_score(self, agent1, agent2):
        # Simulate score based on names
        if "Momentum" in agent1 and "Macro" in agent2:
            return 0.9
        return 0.5

    def propose_co_mutation(self, agent1, agent2):
        proposal = {
            "agents": [agent1.name, agent2.name],
            "proposed_mutation": "Signal fusion with macro filters",
            "rationale": f"{agent1.name} overtrades in volatile conditions; {agent2.name} lacks execution",
            "confidence": 0.88,
            "requires_vote": True
        }
        VaultLogger.log_proposal(proposal)
        return proposal

#####################
# AGENT REGISTRY
#####################
class AgentRegistry:
    @staticmethod
    def crypto_agents(agents):
        # Assume agents with 'Spider' or 'RiskSentinel' are crypto-focused
        return [a for a in agents if 'Spider' in a.name or 'RiskSentinel' in a.name]

    @staticmethod
    def options_agents(agents):
        # Assume agents with 'Momentum' or 'SignalForge' are options-focused
        return [a for a in agents if 'Momentum' in a.name or 'SignalForge' in a.name]

    @staticmethod
    def get_agent_names(agents):
        return [a.name for a in agents]

#####################
# MUTATION GUILD
#####################
class MutationGuild:
    def __init__(self, members):
        self.members = members  # List of agent objects
        self.shared_goals = self.define_goals()
        self.mutation_history = self.aggregate_history()

    def define_goals(self):
        # Simulate shared goals based on member names
        if any("Momentum" in m.name for m in self.members) and any("Macro" in m.name for m in self.members):
            return ["Enhance signal fusion", "Improve volatility handling"]
        return ["General mutation refinement"]

    def aggregate_history(self):
        # Simulate aggregating mutation history
        history = []
        for member in self.members:
            history.extend([f"{member.name} mutation: risk-adjusted"])
        return history

    def propose_guild_mutation(self):
        proposal = {
            "guild": [m.name for m in self.members],
            "proposed_mutation": "Co-mutated agent: MomentumMacroX",
            "rationale": "Combining momentum signals with macro filters for better execution",
            "confidence": 0.92,
            "requires_vote": True
        }
        VaultLogger.log_proposal(proposal)
        return proposal

    def internal_vote(self, proposal):
        # Simulate internal consensus: majority approval
        approvals = len([m for m in self.members if m.performance["accuracy"] > 0.7])
        return approvals > len(self.members) / 2

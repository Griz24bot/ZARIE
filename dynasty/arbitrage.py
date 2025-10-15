import logging
from datetime import datetime
from agents import VaultLogger
from alerts import send_alert

logger = logging.getLogger(__name__)

class ArbitrageScanner:
    def __init__(self, adapters):
        self.adapters = adapters  # Dict like {"Alpaca": AlpacaAdapter(), "Robinhood": RobinhoodAdapter()}

    def scan(self, symbol):
        prices = {}
        for name, adapter in self.adapters.items():
            try:
                bid_ask = adapter.get_best_bid_ask(symbol)
                prices[name] = {
                    "bid": float(bid_ask["bid_price"]),
                    "ask": float(bid_ask["ask_price"])
                }
            except Exception as e:
                logger.warning(f"Failed to get prices for {symbol} on {name}: {e}")
                continue

        # Detect arbitrage opportunities
        opportunities = []
        for src, src_data in prices.items():
            for dst, dst_data in prices.items():
                if src != dst and src_data["ask"] < dst_data["bid"]:
                    spread = dst_data["bid"] - src_data["ask"]
                    opportunities.append({
                        "symbol": symbol,
                        "buy_from": src,
                        "sell_to": dst,
                        "spread": spread,
                        "timestamp": datetime.utcnow().isoformat()
                    })
        return opportunities

    def execute_arbitrage(self, opportunity):
        if opportunity["spread"] > 50:  # Minimum spread threshold
            VaultLogger.log("Arbitrage Opportunity", opportunity)
            send_alert(f"💰 Arbitrage: Buy from {opportunity['buy_from']} → Sell to {opportunity['sell_to']} | Spread: ${opportunity['spread']:.2f}")

            # Execute trades via adapters
            buy_adapter = self.adapters[opportunity["buy_from"]]
            sell_adapter = self.adapters[opportunity["sell_to"]]

            try:
                # Buy from source
                buy_signal = {"symbol": opportunity["symbol"], "action": "buy", "qty": 1}
                buy_adapter.execute(buy_signal)

                # Sell to destination
                sell_signal = {"symbol": opportunity["symbol"], "action": "sell", "qty": 1}
                sell_adapter.execute(sell_signal)

                opportunity["status"] = "Executed"
                VaultLogger.log("Arbitrage Executed", opportunity)

            except Exception as e:
                logger.error(f"Arbitrage execution failed: {e}")
                opportunity["status"] = "Failed"
                VaultLogger.log("Arbitrage Failed", opportunity)

    def trigger_mutation_on_spread(self, opportunity):
        if opportunity["spread"] > 100:
            mutation = {
                "agent": "SpreadSniper",
                "strategy": "Cross-platform arbitrage escalation",
                "symbol": opportunity["symbol"],
                "spread": opportunity["spread"],
                "timestamp": datetime.utcnow().isoformat()
            }
            VaultLogger.log("Mutation Proposed", mutation)
            send_alert(f"🧬 Mutation proposed: {mutation['strategy']} on {mutation['symbol']} due to ${mutation['spread']:.2f} spread")

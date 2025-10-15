import logging
import asyncio
from agents import AlpacaAdapter
from memory import BotMemory

logger = logging.getLogger(__name__)

class DynastyFundingAgent:
    def __init__(self, broker_adapter, memory):
        self.broker = broker_adapter
        self.memory = memory

    def journal_funds(self, from_account, to_account, amount):
        try:
            journal = self.broker.journal_funds(from_account, to_account, amount)
            self.memory.log("Journal Entry", journal["id"])
            logger.info(f"Journal entry created: {journal['id']} from {from_account} to {to_account} for {amount}")
            return journal
        except Exception as e:
            logger.error(f"Journaling failed: {e}")
            raise e

    def place_order(self, account_id, symbol, qty, side="buy"):
        try:
            order = self.broker.place_order(account_id, symbol, qty, side)
            self.memory.log("Order Placed", order["id"])
            logger.info(f"Order placed: {order['id']} for {qty} {symbol} {side}")
            return order
        except Exception as e:
            logger.error(f"Order placement failed: {e}")
            raise e

    async def monitor_journal_events(self, account_id):
        try:
            logger.info(f"Starting journal event monitoring for account {account_id}")
            self.broker.listen_to_journal_events(account_id)
        except Exception as e:
            logger.error(f"Event monitoring failed: {e}")
            raise e

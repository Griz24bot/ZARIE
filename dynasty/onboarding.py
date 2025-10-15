import logging
from agents import AlpacaAdapter
from memory import BotMemory

logger = logging.getLogger(__name__)

class DynastyOnboardingAgent:
    def __init__(self, broker_adapter, memory):
        self.broker = broker_adapter
        self.memory = memory

    def onboard_user(self, user_profile):
        try:
            # Step 1: Create Account
            account = self.broker.create_account(user_profile)
            self.memory.log("Account Created", account["id"])
            logger.info(f"Account created: {account['id']}")

            # Step 2: Create ACH Relationship
            ach = self.broker.create_ach_relationship(account["id"], user_profile["bank"])
            self.memory.log("ACH Linked", ach["id"])
            logger.info(f"ACH relationship created: {ach['id']}")

            # Step 3: Initiate ACH Transfer
            transfer = self.broker.initiate_ach_transfer(account["id"], ach["id"], user_profile.get("funding_amount", 1000))
            self.memory.log("ACH Transfer Initiated", transfer["id"])
            logger.info(f"ACH transfer initiated: {transfer['id']}")

            # Step 4: Notify via Telegram
            from .alerts import alert_telegram
            alert_telegram(f"✅ Account created and funded for {user_profile['contact']['email_address']}")

            return {"account_id": account["id"], "ach_id": ach["id"], "transfer_id": transfer["id"]}
        except Exception as e:
            logger.error(f"Onboarding failed: {e}")
            raise e

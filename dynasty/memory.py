import logging

logger = logging.getLogger(__name__)

class BotMemory:
    def __init__(self):
        self.trade_history = []
        self.task_feedbacks = []
        self.error_count = 0
        self.learning_params = {
            "accuracy_boost": 0.01,  # Increment accuracy per positive trade
            "risk_adjustment": 0.05   # Adjust risk tolerance
        }

    def log_trade(self, trade):
        self.trade_history.append(trade)
        self.learn_from_trade(trade)

    def log_task_feedback(self, feedback):
        self.task_feedbacks.append(feedback)
        self.learn_from_feedback(feedback)

    def learn_from_trade(self, trade):
        # Simple adaptation: If trade is positive, boost accuracy; if negative, adjust risk
        if "Bought" in trade or "Sold" in trade:
            # Assume positive if no "Error"
            if "Error" not in trade:
                self.learning_params["accuracy_boost"] += 0.005
                logger.info(f"[LEARNING] Positive trade: Boosted accuracy to {self.learning_params['accuracy_boost']}")
            else:
                self.learning_params["risk_adjustment"] -= 0.01
                logger.warning(f"[LEARNING] Negative trade: Adjusted risk to {self.learning_params['risk_adjustment']}")
                self.error_count += 1
                if self.error_count >= 3:
                    self.trigger_mutation("execution resilience")
        logger.info(f"[LEARNING] Latest trade outcome: {trade}")

    def learn_from_feedback(self, feedback):
        # Adapt based on task feedback
        if "Completed" in feedback:
            self.learning_params["accuracy_boost"] += 0.002
            logger.info(f"[LEARNING] Task success: Accuracy boosted")
        else:
            self.learning_params["risk_adjustment"] -= 0.005
            logger.info(f"[LEARNING] Task feedback: {feedback}")

    def get_adapted_params(self):
        return self.learning_params

    def trigger_mutation(self, strategy):
        print(f"[MUTATION TRIGGERED] Strategy: {strategy} due to repeated errors.")
        # Simulate mutation logic here

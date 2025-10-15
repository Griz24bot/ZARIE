import logging
from config import MODE, ASSETS

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self, alpaca_api, coinbase_api):
        self.alpaca_api = alpaca_api
        self.coinbase_api = coinbase_api
        self.mode = MODE

    def execute_trade(self, symbol, side, qty, type='market'):
        if self.mode == "paper":
            logger.info(f"[PAPER TRADE] {side} {qty} {symbol}")
            print(f"Paper: {side} {qty} {symbol}")
            return {"status": "paper_executed"}
        elif self.mode == "live":
            return self.alpaca_trade(symbol, side, qty)
        else:
            raise ValueError("Invalid mode")

    def alpaca_trade(self, symbol, side, qty):
        try:
            order = self.alpaca_api.submit_order(symbol=symbol, qty=qty, side=side, type='market', time_in_force='gtc')
            logger.info(f"[ALPACA TRADE] {order}")
            print(f"Alpaca: {side} {qty} {symbol}")
            return order
        except Exception as e:
            logger.error(f"[ALPACA ERROR] {e}")
            print(f"Alpaca Error: {e}")
            return {"error": str(e)}

    def coinbase_trade(self, symbol, side, qty):
        try:
            # Assuming quote_size for simplicity
            quote_size = str(qty * 100)  # Dummy conversion
            order = self.coinbase_api.place_order(
                product_id=symbol,
                side=side,
                order_configuration={
                    "market_market_ioc": {"quote_size": quote_size}
                }
            )
            logger.info(f"[COINBASE TRADE] {order}")
            print(f"Coinbase: {side} {quote_size} USD of {symbol}")
            return order
        except Exception as e:
            logger.error(f"[COINBASE ERROR] {e}")
            print(f"Coinbase Error: {e}")
            return {"error": str(e)}

def moving_average_crossover(api, symbol='AAPL', short_window=5, long_window=20):
    barset = api.get_bars(symbol, '1Min', limit=long_window+1)
    closes = [bar.c for bar in barset]
    if len(closes) < long_window:
        logger.warning(f"Not enough data for {symbol}")
        return None
    short_avg = sum(closes[-short_window:]) / short_window
    long_avg = sum(closes[-long_window:]) / long_window
    position = 0.0
    try:
        pos = api.get_position(symbol)
        position = float(pos.qty)
    except:
        position = 0.0

    if short_avg > long_avg and position == 0:
        return {"action": "buy", "qty": 1}
    elif short_avg < long_avg and position > 0:
        return {"action": "sell", "qty": 1}
    return None

def coinbase_trade(api, symbol='BTC-USD', side='buy', quote_size='100.00'):
    try:
        import uuid
        client_order_id = str(uuid.uuid4())
        order = api.place_order(
            client_order_id=client_order_id,
            product_id=symbol,
            side=side,
            order_configuration={
                "market_market_ioc": {"quote_size": quote_size}
            }
        )
        logger.info(f"[COINBASE TRADE] {order}")
        print(f"Coinbase: {side} {quote_size} USD of {symbol}")
        return order
    except Exception as e:
        logger.error(f"[COINBASE ERROR] {e}")
        print(f"Coinbase Error: {e}")
        return {"error": str(e)}

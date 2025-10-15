import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL')
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_PRIVATE_KEY = os.getenv('COINBASE_PRIVATE_KEY')
NEWSERVICE_API_KEY = os.getenv('NEWSERVICE_API_KEY')

# LLM API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Mode: "paper" or "live"
MODE = os.getenv('MODE', 'live')  # Set to live for live trading

# Assets
STOCK_SYMBOLS = ['AAPL']
CRYPTO_SYMBOLS = ['BTC-USD']
ASSETS = STOCK_SYMBOLS + CRYPTO_SYMBOLS

# Thresholds
MUTATION_DRAW_DOWN_THRESHOLD = 5.0
MUTATION_ACCURACY_THRESHOLD = 0.6
EPOCH_SHIFT_INTERVAL = 60  # minutes
GUILD_PROPOSAL_INTERVAL = 30  # minutes

# Simulation
SIMULATION_DURATION = 180  # minutes (3 hours)

# Logging
LOG_LEVEL = 'INFO'

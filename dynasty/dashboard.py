import pandas as pd
from assets import CryptoAssetRegistry
from agents import VaultLogger

class TradingDashboard:
    def __init__(self):
        self.asset_registry = CryptoAssetRegistry()
        self.agent_status = {}

    def update_agent_status(self, agent_name, status, last_trade=None):
        self.agent_status[agent_name] = {
            "status": status,
            "last_trade": last_trade,
            "platform": "Alpaca" if "Alpaca" in agent_name else "Robinhood"
        }

    def display_dashboard(self):
        print("\n" + "="*80)
        print("DYNASTY TRADING DASHBOARD")
        print("="*80)

        # Asset Coverage
        print("\n📊 ASSET COVERAGE:")
        print(f"Alpaca Assets: {len(self.asset_registry.get_platform_assets('Alpaca'))}")
        print(f"Robinhood Assets: {len(self.asset_registry.get_platform_assets('Robinhood'))}")
        print(f"Common Assets: {len(self.asset_registry.get_common_assets())}")

        # Agent Status Table
        print("\n🤖 AGENT STATUS:")
        print("-" * 60)
        print(f"{'Platform':<12} {'Agent':<15} {'Status':<10} {'Last Trade':<20}")
        print("-" * 60)

        for agent_name, info in self.agent_status.items():
            platform = info['platform']
            status = info['status']
            last_trade = info.get('last_trade', 'N/A')
            print(f"{platform:<12} {agent_name:<15} {status:<10} {str(last_trade)[:19]:<20}")

        # Arbitrage Panel
        print("\n💰 ARBITRAGE OPPORTUNITIES:")
        print("-" * 80)
        print(f"{'Symbol':<10} {'Buy From':<12} {'Sell To':<12} {'Spread':<10} {'Status':<15}")
        print("-" * 80)
        # Note: In a real implementation, you'd track recent opportunities
        print("No recent opportunities")
        print("-" * 80)

        # Mutation Tracker
        print("\n🧬 MUTATION TRACKER:")
        print("-" * 80)
        print(f"{'Agent':<15} {'Trigger':<20} {'Strategy':<25} {'Status':<10}")
        print("-" * 80)
        # Note: In a real implementation, you'd track mutation proposals
        print("No recent mutations")
        print("\n" + "="*80)

    def log_trade_summary(self, agent_name, asset, action, qty):
        trade_info = f"{action} {qty} {asset}"
        self.update_agent_status(agent_name, "Active", trade_info)
        VaultLogger.log_trade(f"Dashboard: {agent_name} - {trade_info}")

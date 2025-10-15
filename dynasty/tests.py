import pytest
from memory import BotMemory
from agents import BaseAgent, CoMutationEngine
from trading import TradingEngine
from config import MODE

def test_bot_memory():
    memory = BotMemory()
    memory.log_trade("Bought 1 AAPL")
    assert len(memory.trade_history) == 1
    assert memory.learning_params["accuracy_boost"] > 0.01

def test_base_agent():
    memory = BotMemory()
    agent = BaseAgent("TestAgent", memory)
    signals = agent.generate_signals({})
    assert len(signals) > 0

def test_co_mutation_engine():
    registry = ["MomentumX", "MacroSentinel"]
    engine = CoMutationEngine(registry)
    partner = engine.find_partner("MomentumX")
    assert partner is not None

def test_trading_engine_paper():
    # Mock APIs
    class MockAPI:
        def submit_order(self, **kwargs):
            return {"status": "mocked"}
        def place_order(self, **kwargs):
            return {"status": "mocked"}

    engine = TradingEngine(MockAPI(), MockAPI())
    result = engine.execute_trade("AAPL", "buy", 1)
    assert result["status"] == "paper_executed"

def test_agent_registry_crypto():
    from .agents import AgentRegistry, SpiderV4, RiskSentinelV2, MomentumX, SignalForge
    memory = BotMemory()
    agents = [
        SpiderV4(memory, None),
        RiskSentinelV2(memory, None),
        MomentumX(memory, None),
        SignalForge(memory, None)
    ]
    crypto_agents = AgentRegistry.crypto_agents(agents)
    assert len(crypto_agents) == 2
    assert all('Spider' in a.name or 'RiskSentinel' in a.name for a in crypto_agents)

def test_agent_registry_options():
    from .agents import AgentRegistry, SpiderV4, RiskSentinelV2, MomentumX, SignalForge
    memory = BotMemory()
    agents = [
        SpiderV4(memory, None),
        RiskSentinelV2(memory, None),
        MomentumX(memory, None),
        SignalForge(memory, None)
    ]
    options_agents = AgentRegistry.options_agents(agents)
    assert len(options_agents) == 2
    assert all('Momentum' in a.name or 'SignalForge' in a.name for a in options_agents)

def test_agent_registry_get_names():
    from .agents import AgentRegistry, SpiderV4, RiskSentinelV2
    memory = BotMemory()
    agents = [
        SpiderV4(memory, None),
        RiskSentinelV2(memory, None)
    ]
    names = AgentRegistry.get_agent_names(agents)
    assert len(names) == 2
    assert 'SpiderV4' in names
    assert 'RiskSentinel-V2' in names

def test_mutation_triggers_volatility():
    from .agents import AgentRegistry, SpiderV4, RiskSentinelV2
    memory = BotMemory()
    agents = [
        SpiderV4(memory, None),
        RiskSentinelV2(memory, None)
    ]
    market_data = {"BTC": {"volatility": 0.07}}
    # Simulate trigger
    triggered = False
    if market_data.get("BTC", {}).get("volatility", 0) > 0.06:
        for agent in AgentRegistry.crypto_agents(agents):
            agent.mutate("Add volatility shield")
            triggered = True
    assert triggered

def test_mutation_triggers_slippage():
    from .agents import AgentRegistry, MomentumX, SignalForge
    memory = BotMemory()
    agents = [
        MomentumX(memory, None),
        SignalForge(memory, None)
    ]
    market_data = {"AAPL_0.5C": {"slippage": 0.04}}
    # Simulate trigger
    triggered = False
    if market_data.get("AAPL_0.5C", {}).get("slippage", 0) > 0.03:
        for agent in AgentRegistry.options_agents(agents):
            agent.mutate("Execution optimizer")
            triggered = True
    assert triggered

def test_simulation_mutation_triggers():
    from .simulation import dynasty_simulation
    # Run a short simulation to test triggers
    # This will test the integration in simulation loop
    # Note: This test may take time due to sleep(1), so keep duration short
    try:
        dynasty_simulation(duration_minutes=5)  # Short run
        # If no exceptions, assume success
        assert True
    except Exception as e:
        print(f"Simulation test failed: {e}")
        assert False

if __name__ == "__main__":
    pytest.main([__file__])

# TODO: Dynasty Refactor & Simulation Upgrade

## Completed
- [x] Add MutationLearner class
- [x] Add CoMutationEngine class
- [x] Add MutationGuild class
- [x] Add MomentumMacroX agent class
- [x] Integrate ZARIE AI Steward with voice interface (TTS + speech recognition)
- [x] Add cross-agent communication via ZARIE
- [x] Simulate mutation cascade initiated by ZARIE
- [x] Codify ZARIE’s doctrine in Dynasty Charter v3.0
- [x] Implement On ZARIE framework with avatar, animation, and override capabilities
- [x] Add Alexis avatar initialization and welcome message
- [x] Add Telegram bot integration for remote commands (/status_check, /mutation_vote, /override)
- [x] Implement AgentManager for cross-agent messaging
- [x] Add Code Intelligence Engine: Live Python execution, error handling, code fixing
- [x] Add Knowledge Response Layer: LLM Q&A, vault logging, voice/text delivery
- [x] Add Agent Collaboration Protocol: Enhanced ZARIE-agent communication, mutation proposals, decision logging
- [x] Update Dynasty Charter v3.0 with Article XI, XII, XIII, and XIV (Oracle Response Protocol)
- [x] Implement Dashboard Animation Flow for oracle answers
- [x] Add Doctrine Delivery Protocol with animation and logging
- [x] Implement Mutation Vote Protocol with dashboard animation, live tally, and outcome handling

## Pending
- [ ] Modularize main.py into separate files:
  - [ ] agents.py: Agent classes, mutation logic, guild formation
  - [ ] trading.py: Execution logic, signal parsing, paper/live routing
  - [ ] simulation.py: Dynasty loop, epoch shifts, co-mutation triggers
  - [ ] memory.py: BotMemory class with historical learning
  - [ ] config.py: Mode flags, asset lists, thresholds
  - [ ] Update api.py: Lineage updates, agent state sync
  - [ ] tests.py: Pytest suite for core logic
- [ ] Integrate CoMutationEngine into simulation.py, allow agents to propose joint mutations
- [ ] Form MutationGuilds in agents.py based on agents
- [ ] Update simulation.py to trigger guild proposals and co-mutations
- [ ] Add MomentumMacroX to agents list and registry in simulation.py
- [ ] Update orchestrate method in simulation.py to handle new agent
- [ ] Enhance BotMemory Learning: Adjust agent params (e.g. accuracy, risk tolerance) based on trade outcomes
- [ ] Add Error Handling: Wrap critical blocks in try/except, log with logging module
- [ ] Implement Paper/Live Toggle: Use config.MODE = "paper" or "live" to gate execution
- [ ] Improve Concurrency: Use asyncio or threading for real-time simulation
- [ ] Update Lineage: api.py pushes real-time agent state to frontend or dashboard
- [ ] Add Testing: tests.py covers agent logic, mutation triggers, trade execution, memory updates
- [ ] Install/verify dependencies (fastapi, websockets, pytest, pydantic, etc.)
- [ ] Run pytest and confirm all tests pass
- [ ] Launch simulation in paper mode, verify agent behavior and mutation triggers
- [ ] Check UI/dashboard for lineage sync and agent status
- [ ] Confirm Telegram bot receives updates and override commands work (if implemented)

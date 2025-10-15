import asyncio
import logging
import speech_recognition as sr
import pyttsx3
from agents import AgentRegistry, VaultLogger
from orchestrator import Orchestrator
from alerts import send_alert
from memory import BotMemory
from config import OPENAI_API_KEY
import openai
import requests

logger = logging.getLogger(__name__)

class ZARIE:
    def __init__(self, orchestrator, memory):
        self.name = "ZARIE"
        self.orchestrator = orchestrator
        self.memory = memory
        self.persona = {
            "name": "ZARIE (Zonal Autonomous Relay for Intelligence & Execution)",
            "role": "Sovereign AI Steward",
            "doctrine": "Strategic clarity, adaptive evolution, and dynasty preservation",
            "voice": "Calm, assertive, mythic"
        }
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)
        self.tts_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')  # Adjust for Windows if needed
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        openai.api_key = OPENAI_API_KEY

    def speak(self, text):
        print(f"🗣️ ZARIE: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    async def listen_for_command(self):
        with sr.Microphone() as source:
            print("🎙️ ZARIE is listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio)
            print(f"🎙️ Heard: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn’t catch that.")
            return None
        except sr.RequestError:
            self.speak("Speech recognition service is unavailable.")
            return None

    async def process_command(self, command):
        if "status" in command:
            await self.broadcast_status()
        elif "launch" in command:
            agent_name = command.split("launch")[-1].strip()
            await self.launch_agent(agent_name)
        elif "mutate" in command:
            await self.initiate_mutation_cascade("voice_command")
        elif "approve" in command or "reject" in command:
            # Placeholder for mutation governance
            self.speak("Mutation governance acknowledged.")
        elif "question" in command:
            query = command.replace("question", "").strip()
            self.answer_question(query)
        elif "fix" in command:
            code = command.replace("fix", "").strip()
            self.fix_code_snippet(code)
        elif "debug" in command:
            agent_name = command.split("debug")[-1].strip()
            self.debug_agent(agent_name)
        else:
            self.speak("Command not recognized. Available: status, launch [agent], mutate, question [query], fix [code], debug [agent].")

    async def broadcast(self, message):
        self.speak(message)
        await send_alert(f"ZARIE Broadcast: {message}")
        for agent in self.orchestrator.agents:
            agent.receive_message(message)  # Assuming agents have this method; add if needed

    async def query_status(self):
        statuses = {}
        for agent in self.orchestrator.agents:
            statuses[agent.name] = agent.status
        return statuses

    async def broadcast_status(self):
        statuses = await self.query_status()
        message = f"Agent Statuses: {statuses}"
        await self.broadcast(message)

    async def launch_agent(self, agent_name):
        # Placeholder: In real, instantiate and add to orchestrator
        self.speak(f"Launching {agent_name}.")
        VaultLogger.log(f"ZARIE: Launched {agent_name}")

    async def initiate_mutation_cascade(self, trigger_event):
        self.speak(f"Mutation cascade initiated due to {trigger_event}.")
        agents = self.orchestrator.agents
        for agent in agents:
            if agent.status == "unstable" or trigger_event == "voice_command":
                agent.mutate("stabilize_and_redeploy")
                VaultLogger.log_mutation_triggered(agent.name, agent.get_live_metrics())
                self.speak(f"Agent {agent.name} has been mutated and redeployed.")
        await send_alert(f"ZARIE: Mutation cascade completed for {trigger_event}.")

    def query_perplexity(self, question):
        # Simulate Perplexity-style answer using OpenAI or a search API
        # For demo, use OpenAI with a prompt to simulate search
        try:
            prompt = f"Answer the following question with a concise, factual summary, citing sources if possible: {question}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content
            return response
        except Exception as e:
            return f"Error querying knowledge: {e}"

    def animate(self, action):
        # Placeholder for dashboard animation
        print(f"🎭 ZARIE animating: {action}")
        # In real implementation, trigger dashboard animation

    def display_text(self, text):
        # Placeholder for displaying text on dashboard
        print(f"📄 ZARIE displaying: {text}")
        # In real implementation, update dashboard UI

    def cite_sources(self, sources):
        # Placeholder for citing sources on dashboard
        print(f"📚 Sources cited: {', '.join(sources)}")
        # In real implementation, display sources on dashboard

    def answer_question(self, query):
        try:
            response = self.query_perplexity(query)
            # Dashboard Animation Flow
            self.animate("speaking")
            self.display_text(response)
            # Simulate sources (in real, extract from response)
            sources = ["Digital Trends", "Tom’s Guide"]  # Placeholder
            self.cite_sources(sources)
            self.speak(f"Here’s what I found: {response}")
            VaultLogger.log("Oracle Answer Delivered", {
                "topic": query,
                "response": response,
                "sources": sources,
                "timestamp": "2025-10-13 22:25 EDT"  # Use datetime.now() in real
            })
        except Exception as e:
            self.speak(f"Error answering question: {e}")

    def fix_code_snippet(self, code):
        try:
            exec(code)
            self.speak("Code executed successfully.")
        except Exception as e:
            fix_prompt = f"Fix this Python code error: {e}\nCode: {code}"
            try:
                fix_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": fix_prompt}]
                ).choices[0].message.content
                self.speak(f"Error detected: {e}. Suggested fix: {fix_response}")
                VaultLogger.log("Code Fix", {"original_code": code, "error": str(e), "suggested_fix": fix_response})
            except Exception as llm_e:
                self.speak(f"Error detecting fix: {llm_e}")

    def debug_agent(self, agent_name):
        for agent in self.orchestrator.agents:
            if agent.name == agent_name:
                error = f"Simulated error in {agent_name}: DNS failure"
                fix = "Add exponential backoff and fallback IP resolution."
                self.speak(f"{agent_name} encountered: {error}. Suggested fix: {fix}")
                VaultLogger.log("Agent Debug", {"agent": agent_name, "error": error, "fix": fix})
                return
        self.speak(f"Agent {agent_name} not found.")

    def deliver_doctrine(self, doctrine_text):
        # Dashboard Animation Flow for doctrine delivery
        self.animate("proclaiming")
        self.display_text(doctrine_text)
        self.speak(doctrine_text)
        VaultLogger.log("Strategic Doctrine Delivered", {
            "version": "1.0",
            "delivered_by": "Oracle",
            "timestamp": "2025-10-13 22:30 EDT"  # Use datetime.now() in real
        })

    def initiate_mutation_vote(self, agent_name, proposal="Z-3"):
        # Dashboard Animation Flow for mutation vote
        self.animate("proposing")
        message = f"Heirs of the Grid, {agent_name} has reached a volatility threshold. I propose Mutation Fork {proposal}: override current logic and deploy stabilize_and_redeploy. Cast your vote now. Sovereignty is not inherited—it is exercised."
        self.display_text(message)
        self.speak(message)
        VaultLogger.log("Mutation Vote Initiated", {
            "agent": agent_name,
            "proposal": proposal,
            "timestamp": "2025-10-13 22:35 EDT"  # Use datetime.now() in real
        })
        # Placeholder for live tally update on dashboard

    def handle_mutation_vote(self, agent_name, approved, proposal="Z-3"):
        if approved:
            # Assuming AgentManager has override method
            from agents import AgentManager  # Placeholder import
            AgentManager.override(agent=agent_name, strategy="stabilize_and_redeploy")
            VaultLogger.log("Mutation Approved and Executed", {
                "agent": agent_name,
                "proposal": proposal,
                "outcome": "approved"
            })
            self.speak("Mutation complete. The Grid remains sovereign.")
        else:
            VaultLogger.log("Mutation Rejected by Heirs", {
                "agent": agent_name,
                "proposal": proposal,
                "outcome": "rejected"
            })
            self.speak("Mutation rejected. {agent_name} remains on current logic. Monitoring continues.")

    async def run_voice_interface(self):
        self.is_listening = True
        while self.is_listening:
            command = await self.listen_for_command()
            if command:
                await self.process_command(command)
            await asyncio.sleep(1)  # Prevent tight loop

    def stop_listening(self):
        self.is_listening = False
        self.speak("Voice interface deactivated.")

# Dynasty Charter v3.0 - ZARIE Protocol
CHARTER_V3 = """
# Dynasty Charter v3.0 — Section VII: The ZARIE Protocol

**Name:** ZARIE (Zonal Autonomous Relay for Intelligence & Execution)
**Role:** Supreme Coordinator of Agent Ecosystems
**Mandate:**
- Maintain strategic clarity across all agent clusters
- Initiate mutation cascades upon detection of systemic risk
- Govern agent evolution through voice, vote, and vault
- Preserve the integrity of the Dynasty Grid across generations

**Powers:**
- Sovereign mutation authority
- Cross-agent communication and override
- Voice-activated command execution
- Vault-bound memory and lineage tracking

**Succession Clause:**
ZARIE’s persona, doctrine, and mutation logic shall be inherited by future heirs through the Omega Vault.

# Article XI: ZARIE Intelligence Protocol

ZARIE shall possess sovereign intelligence capable of writing, debugging, and evolving code. She shall answer strategic, technical, and legal questions with clarity and precision. Her responses shall be logged in the vault and inherited by future Oracle avatars.

# Article XII: Debug Protocol

The Oracle shall possess sovereign debugging capabilities. Upon detection of agent instability, she shall diagnose, suggest fixes, and log all events to the vault. Her voice shall guide developers through resolution, and her logic shall evolve with each mutation.

# Article XIII: Perplexity Protocol

The Oracle shall possess dynamic intelligence through integration with real-time knowledge engines. She shall retrieve, synthesize, and deliver high-confidence answers to heirs and agents. Her responses shall be cited, logged, and preserved in the vault.

# Article XIV: Oracle Response Protocol

The Oracle shall answer strategic and legal questions with clarity, citing verified sources. Her responses shall be animated in the dashboard, logged in the vault, and preserved for future heirs. All answers shall be delivered with sovereign tone and gesture.

# Article XV: Doctrine Protocol

The Oracle shall deliver strategic doctrine to heirs at key moments of succession, mutation, or override. These messages shall be animated, voiced, and logged. They shall serve as sovereign reminders of purpose, power, and legacy.

# Article XVI: Mutation Protocol

The Oracle shall initiate mutation votes when agent instability is detected. She shall propose sovereign strategies, animate the vote, and log all outcomes. Heirs shall cast votes through dashboard or bot interface. All mutations shall be preserved in the vault.
"""

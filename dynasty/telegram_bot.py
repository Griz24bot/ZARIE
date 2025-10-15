import logging
import asyncio
from on_zarie import OnZARIE
from agents import AgentRegistry, VaultLogger

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, zarie, orchestrator):
        self.zarie = zarie
        self.orchestrator = orchestrator
        self.bot_token = "7575096974:AAGn1yVwkaNbsNFYHkz6cvPq6crAWkMaoeE"  # Real token
        self.chat_id = None  # Will be set when message received
        from telegram import Bot
        self.bot = Bot(token=self.bot_token)

    async def send_message(self, message):
        # Simulate sending message to Telegram
        print(f"📱 Telegram Bot: {message}")
        logger.info(f"Telegram message sent: {message}")

    async def handle_command(self, command):
        if command == "/status_check":
            statuses = await self.zarie.query_status()
            message = f"Agent Statuses: {statuses}"
            await self.send_message(message)
        elif command == "/mutation_vote":
            # Simulate mutation vote initiation
            self.zarie.speak("Mutation vote initiated. Heirs, cast your votes.")
            VaultLogger.log("Mutation vote initiated via Telegram")
            await self.send_message("Mutation vote initiated.")
        elif command.startswith("/override"):
            parts = command.split()
            if len(parts) >= 3:
                agent = parts[1]
                protocol = parts[2]
                self.zarie.override(agent, f"protocol {protocol}")
                message = f"Override {protocol} executed on {agent}."
                await self.send_message(message)
        else:
            await self.send_message("Unknown command.")

    async def poll_updates(self):
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        application = Application.builder().token(self.bot_token).build()

        async def status_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            statuses = await self.zarie.query_status()
            message = f"Agent Statuses: {statuses}"
            await update.message.reply_text(message)

        async def mutation_vote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.zarie.speak("Mutation vote initiated. Heirs, cast your votes.")
            VaultLogger.log("Mutation vote initiated via Telegram")
            await update.message.reply_text("Mutation vote initiated.")

        async def override(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            args = context.args
            if len(args) >= 2:
                agent = args[0]
                protocol = args[1]
                self.zarie.override(agent, f"protocol {protocol}")
                message = f"Override {protocol} executed on {agent}."
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Usage: /override <agent> <protocol>")

        async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            query = ' '.join(context.args)
            if query:
                self.zarie.answer_question(query)
                await update.message.reply_text("Question processed. Check ZARIE's response.")
            else:
                await update.message.reply_text("Usage: /question <your query>")

        async def fix(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            code = ' '.join(context.args)
            if code:
                self.zarie.fix_code_snippet(code)
                await update.message.reply_text("Code fix processed. Check ZARIE's response.")
            else:
                await update.message.reply_text("Usage: /fix <code snippet>")

        async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            agent_name = ' '.join(context.args)
            if agent_name:
                self.zarie.debug_agent(agent_name)
                await update.message.reply_text("Debug processed. Check ZARIE's response.")
            else:
                await update.message.reply_text("Usage: /debug <agent_name>")

        application.add_handler(CommandHandler("status_check", status_check))
        application.add_handler(CommandHandler("mutation_vote", mutation_vote))
        application.add_handler(CommandHandler("override", override))
        application.add_handler(CommandHandler("question", question))
        application.add_handler(CommandHandler("fix", fix))
        application.add_handler(CommandHandler("debug", debug))

        await application.run_polling()

# AgentManager for cross-agent messaging
class AgentManager:
    @staticmethod
    def send_message(from_agent, to_agent, message):
        print(f"📨 Message from {from_agent} to {to_agent}: {message}")
        # In real, route to specific agent
        if to_agent == "ZARIE":
            # Assuming zarie is accessible
            pass  # ZARIE.respond would be called here

    @staticmethod
    def broadcast(message):
        print(f"📢 Broadcast: {message}")
        # Broadcast to all agents

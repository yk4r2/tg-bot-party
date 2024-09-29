import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, MessageHandler, filters
from config import BOT_TOKEN
from modules import handlers

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("register", handlers.register))
    application.add_handler(CommandHandler("role", handlers.get_role))
    application.add_handler(CommandHandler("info", handlers.get_info))
    application.add_handler(CommandHandler("mission", handlers.get_mission))

    # Chat member handlers
    application.add_handler(ChatMemberHandler(handlers.track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(handlers.greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

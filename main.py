import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from config import TOKEN
from handlers import start, handle_name, handle_contact, handle_admin_command, handle_text
from database import init_db

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
NAME, CONTACT = range(2)

def main():
    # Initialize the database
    init_db()

    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TOKEN).build()

    # Add conversation handler with the states NAME and CONTACT
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact)]
        },
        fallbacks=[]
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('admin', handle_admin_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()

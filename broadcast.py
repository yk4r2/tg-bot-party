import sys
from telegram.ext import Application
from config import BOT_TOKEN
from modules.storage import get_all_user_ids

async def send_broadcast(message: str):
    application = Application.builder().token(BOT_TOKEN).build()
    user_ids = get_all_user_ids()
    
    for user_id in user_ids:
        try:
            await application.bot.send_message(chat_id=user_id, text=message)
            print(f"Message sent to user {user_id}")
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python broadcast.py 'Your message here'")
    else:
        message = " ".join(sys.argv[1:])
        import asyncio
        asyncio.run(send_broadcast(message))

from telegram import Update, Chat, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from modules import storage, utils
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if storage.user_exists(user_id):
        await update.message.reply_text("Welcome back, operative. Use /role to see your assignment.")
    else:
        await update.message.reply_text("Greetings, new recruit. Use /register to join the operation.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if storage.user_exists(user_id):
        await update.message.reply_text("You're already registered, operative.")
    else:
        role = utils.assign_role()
        storage.save_user(user_id, role)
        await update.message.reply_text(f"Registration complete. Your role: {role}")

async def get_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = storage.get_user(user_id)
    if user:
        await update.message.reply_text(f"Your current role: {user['role']}")
    else:
        await update.message.reply_text("You're not registered. Use /register to join.")

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info = utils.get_event_info()
    await update.message.reply_text(info)

async def get_mission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mission = utils.get_mission_briefing()
    await update.message.reply_text(mission)

async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = utils.extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    cause_name = update.effective_user.full_name
    chat = update.effective_chat

    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s unblocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)

async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = utils.extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        await update.effective_chat.send_message(
            f"{member_name} has infiltrated our network. Welcome, operative!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            f"{member_name} has been disconnected from the grid. Farewell, operative.",
            parse_mode=ParseMode.HTML,
        )

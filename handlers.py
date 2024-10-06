from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import add_or_update_user, get_user, update_user_role, get_all_users
from utils import send_invitation, send_group_message, export_users_to_excel
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define conversation states
NAME, CONTACT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for the user's name."""
    await update.message.reply_text("Привет. Пожалуйста, назови свои имя и фамилию.")
    return NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    name = update.message.text
    first_name, last_name = name.split(maxsplit=1)
    
    if user.username:
        add_or_update_user(user.id, user.username, None, first_name, last_name)
        await update.message.reply_text(f"Рады знакомству, {user.username}. Хакерская комиссия рассматривает твою кандидатуру.")
        return ConversationHandler.END
    else:
        context.user_data['name'] = (first_name, last_name)
        await update.message.reply_text("Твой username скрыт. Пожалуйста, оставь свой контакт:")
        return CONTACT

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    contact = update.message.text
    first_name, last_name = context.user_data['name']
    
    add_or_update_user(user.id, None, contact, first_name, last_name)
    await update.message.reply_text(f"Рады знакомству, {first_name}. Хакерская комиссия рассматривает твою кандидатуру.")
    return ConversationHandler.END

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin commands."""
    user = update.effective_user
    if user.username != 'yk4r2':  # Replace with actual admin username
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    command = context.args[0] if context.args else None
    if command == 'invite':
        await send_invitation(context)
    elif command == 'group_message':
        group = context.args[1]
        message = ' '.join(context.args[2:])
        await send_group_message(context, group, message)
    elif command == 'update_role':
        user_id = int(context.args[1])
        role = context.args[2]
        update_user_role(user_id, role)
        await update.message.reply_text(f"Роль пользователя {user_id} обновлена на {role}")
    elif command == 'export_users':
        file_path = export_users_to_excel()
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))
    elif command == 'check_support_requests':
        requests = get_open_support_requests()
        if requests:
            message = "Open support requests:\n\n"
            for req in requests:
                user = get_user(req.user_id)
                message += f"User: {user.username or user.first_name}\n"
                message += f"Request: {req.request_text}\n"
                message += f"Created at: {req.created_at}\n\n"
        else:
            message = "No open support requests."
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Неизвестная команда. Доступные команды: invite, group_message, update_role, export_users")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    user = update.effective_user
    text = update.message.text
    logger.info(f"Received message from {user.username}: {text}")
    # Add any additional text handling logic here

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import add_or_update_user, get_user, update_user_role, get_all_users
from utils import send_invitation, send_group_message, export_users_to_excel, send_group_message, send_personal_message
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
        await send_group_message(context, group, 'custom_group_message', message=message)
    elif command == 'preparation_reminder':
        await send_group_message(context, 'all', 'preparation_reminder')
    elif command == 'event_start':
        await send_group_message(context, 'all', 'event_start')
    elif command == 'victory_announcement':
        await send_group_message(context, 'all', 'victory_announcement')
    elif command == 'jam_session':
        await send_group_message(context, 'all', 'jam_session')
    elif command == 'update_role':
        user_id = int(context.args[1])
        role = context.args[2]
        update_user_role(user_id, role)
        await update.message.reply_text(f"Роль пользователя {user_id} обновлена на {role}")
    elif command == 'export_users':
        file_path = export_users_to_excel()
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))
    elif command == 'send_personal':
        user_id = int(context.args[1])
        template_name = context.args[2]
        await send_personal_message(context, user_id, template_name)
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


async def send_to_admin(context: ContextTypes.DEFAULT_TYPE, user_id: int, username: str, message: str):
    admin_username = 'yk4r2'  # Replace with the actual admin username
    admin_user = await context.bot.get_chat(admin_username)
    if admin_user:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        admin_message = f"{user_id} | {username} | {current_time} | {message}\n"
        await context.bot.send_message(chat_id=admin_user.id, text=admin_message)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    user = update.effective_user
    text = update.message.text
    logger.info(f"Received message from {user.username or user.first_name}: {text}")
    await send_to_admin(context, user.id, user.username or user.first_name, text)
    await update.message.reply_text("Спасибо за ваше сообщение. Организаторы свяжутся с вами, если потребуется.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = get_user(user.id)
    role = db_user.role if db_user else "Не назначена"
    await send_personal_message(context, user.id, 'help_message', role=role)

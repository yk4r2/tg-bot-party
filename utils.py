import pandas as pd
from database import get_all_users, get_message_template

async def send_invitation(context):
    users = get_all_users()
    for user in users:
        if user.role == 'defender':
            template = get_message_template('defender_invitation')
        elif user.role == 'hacker':
            template = get_message_template('hacker_invitation')
        else:
            template = get_message_template('non_invitation')
        
        message = template.format(username=user.username or user.first_name)
        await context.bot.send_message(chat_id=user.telegram_id, text=message)

async def send_group_message(context, group, message):
    users = get_all_users()
    for user in users:
        if user.role == group:
            await context.bot.send_message(chat_id=user.telegram_id, text=message)

def export_users_to_excel():
    users = get_all_users()
    df = pd.DataFrame([
        {
            'Telegram ID': user.telegram_id,
            'Username': user.username,
            'Phone': user.phone,
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'Role': user.role,
            'Invited': user.invited,
            'Registration Date': user.registration_date
        }
        for user in users
    ])
    file_path = 'users_export.xlsx'
    df.to_excel(file_path, index=False)
    return file_path

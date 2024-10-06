import pandas as pd
from database import get_all_users, get_message_template, get_user

async def send_invitation(context):
    users = get_all_users()
    for user in users:
        if user.role == 'defender':
            template = get_message_template('defender_invitation')
        elif user.role == 'hacker':
            template = get_message_template('hacker_invitation')
        elif user.role == 'organizer':
            template = get_message_template('organizer_invitation')
        else:
            template = get_message_template('non_invitation')
        
        message = template.format(username=user.username or user.first_name)
        await context.bot.send_message(chat_id=user.telegram_id, text=message)

async def send_group_message(context, group, template_name, **kwargs):
    users = get_all_users()
    template = get_message_template(template_name)
    if not template:
        raise ValueError(f"Template '{template_name}' not found")
    
    for user in users:
        if group == 'all' or user.role == group:
            message = template.format(username=user.username or user.first_name, **kwargs)
            await context.bot.send_message(chat_id=user.telegram_id, text=message)

async def send_personal_message(context, user_id, template_name, **kwargs):
    user = get_user(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    
    template = get_message_template(template_name)
    if not template:
        raise ValueError(f"Template '{template_name}' not found")
    
    message = template.format(username=user.username or user.first_name, **kwargs)
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

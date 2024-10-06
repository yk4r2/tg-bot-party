import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot API Token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///event_bot.db')

# Admin username
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'yk4r2')

# Event details
EVENT_DATE = os.getenv('EVENT_DATE', '19 октября')
EVENT_TIME = os.getenv('EVENT_TIME', '20:00 по 23:00')
EVENT_ADDRESS = os.getenv('EVENT_ADDRESS', 'Dance First, Павелецкая: https://yandex.lt/maps/-/CDThMYN5')
EVENT_CALENDAR_LINK = os.getenv('EVENT_CALENDAR_LINK', 'https://calendar.app.google/cqWteMQQXhgcyhfP6')
GIFT_CHAT_LINK = os.getenv('GIFT_CHAT_LINK', 'https://t.me/+na5kKl-j-JI1Yjky')

# Message templates
TEMPLATES = {
    'initial_greeting': 'Привет. Пожалуйста, назови свои имя и фамилию.',
    'request_contact': 'Твой username скрыт. Пожалуйста, оставь свой контакт:',
    'registration_confirmation': 'Рады знакомству, {username}. Хакерская комиссия рассматривает твою кандидатуру.',
    'defender_invitation': f'''Привет {{username}}. Твоя роль -- defender.

День Рождения пройдёт {EVENT_DATE} с {EVENT_TIME} по адресу {EVENT_ADDRESS}.
Ссылка на google calendar: {EVENT_CALENDAR_LINK}.
Если ты хочешь централизованно что-то подарить, или обсудить идею подарка, вступай в чат: {GIFT_CHAT_LINK}.

В случае если ты не сможешь прийти, обязательно напиши @{ADMIN_USERNAME}, он уберёт тебя из списков.

Хочешь перейти на тёмную сторону силы и помочь хакерам с организацией?
Пиши @{ADMIN_USERNAME}.''',
    'hacker_invitation': f'''Привет {{username}}. Ты уже знаешь, какова твоя роль, hacker.

День Рождения пройдёт {EVENT_DATE} с {EVENT_TIME} по адресу {EVENT_ADDRESS}.
Ссылка на google calendar: {EVENT_CALENDAR_LINK}.
Если ты хочешь централизованно что-то подарить, или обсудить идею подарка, вступай в чат: {GIFT_CHAT_LINK}.

Пиши @{ADMIN_USERNAME}, если тебе не написали ранее.''',
    'non_invitation': '''Привет {username}.

К сожалению, места закончились. Но Оля будет ждать тебя на своем тематическом открытом классе в MDC 18 октября в 19:00 по адресу М. Новокузнецкая; Пятницкая ул., д.6/1, стр.8. Ещё Оля дарит тебе скидку 20% на следующий Мастер-Класс!'''
}

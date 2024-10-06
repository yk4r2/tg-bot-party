import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import TEMPLATES
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    phone = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String)
    invited = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=datetime.utcnow)

class MessageTemplate(Base):
    __tablename__ = 'message_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)

class SupportRequest(Base):
    __tablename__ = 'support_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    request_text = Column(String)
    status = Column(String, default='open')
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///event_bot.db')
Session = sessionmaker(bind=engine)

def init_message_templates():
    session = Session()
    for name, content in TEMPLATES.items():
        template = session.query(MessageTemplate).filter_by(name=name).first()
        if template:
            template.content = content
        else:
            template = MessageTemplate(name=name, content=content)
            session.add(template)
    session.commit()
    session.close()

def init_db():
    Base.metadata.create_all(engine)
    init_message_templates()

def add_or_update_user(telegram_id, username, phone, first_name, last_name):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.username = username
        user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
    else:
        user = User(telegram_id=telegram_id, username=username, phone=phone, first_name=first_name, last_name=last_name)
        session.add(user)
    session.commit()
    session.close()

def add_user(telegram_id, username, phone, first_name, last_name):
    session = Session()
    user = User(telegram_id=telegram_id, username=username, phone=phone, first_name=first_name, last_name=last_name)
    session.add(user)
    session.commit()
    session.close()

def get_user(telegram_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    session.close()
    return user

def update_user_role(telegram_id, role):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.role = role
        session.commit()
    session.close()

def get_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def add_message_template(name, content):
    session = Session()
    template = MessageTemplate(name=name, content=content)
    session.add(template)
    session.commit()
    session.close()

def get_message_template(name):
    session = Session()
    template = session.query(MessageTemplate).filter_by(name=name).first()
    session.close()
    return template.content if template else None

def add_support_request(user_id, request_text):
    session = Session()
    request = SupportRequest(user_id=user_id, request_text=request_text)
    session.add(request)
    session.commit()
    session.close()

def get_open_support_requests():
    session = Session()
    requests = session.query(SupportRequest).filter_by(status='open').all()
    session.close()
    return requests

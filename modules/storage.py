import json
import os
from contextlib import contextmanager
from config import DATA_FILE

LOCK_FILE = DATA_FILE + ".lock"

@contextmanager
def file_lock():
    while os.path.exists(LOCK_FILE):
        time.sleep(0.1)
    try:
        open(LOCK_FILE, 'w').close()
        yield
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

def save_user(user_id: int, role: str):
    with file_lock():
        users = load_users()
        users[str(user_id)] = {"role": role}
        with open(DATA_FILE, 'w') as f:
            json.dump(users, f)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def user_exists(user_id: int) -> bool:
    users = load_users()
    return str(user_id) in users

def get_user(user_id: int):
    users = load_users()
    return users.get(str(user_id))

def get_all_user_ids() -> list:
    return list(load_users().keys())

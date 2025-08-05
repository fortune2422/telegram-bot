import json
import os

DATA_FILE = "accounts.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def is_registered(user_id: int) -> bool:
    data = load_data()
    return str(user_id) in data

def save_account(user_id: int, username: str, password: str):
    data = load_data()
    data[str(user_id)] = {"username": username, "password": password}
    save_data(data)

def load_account(user_id: int):
    data = load_data()
    acc = data.get(str(user_id))
    if acc:
        return acc["username"], acc["password"]
    return None, None

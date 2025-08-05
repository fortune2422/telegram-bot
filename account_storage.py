import json
import os
from datetime import datetime

ACCOUNTS_FILE = "accounts.json"

# 保存账号到 JSON

def save_account(user_id: int, username: str, password: str, file_path=ACCOUNTS_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[str(user_id)] = {
        "username": username,
        "password": password,
        "created_at": datetime.now().isoformat()
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# 读取指定用户账号

def load_account(user_id: int, file_path=ACCOUNTS_FILE):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

    return data.get(str(user_id))


def load_all_accounts(file_path=ACCOUNTS_FILE):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

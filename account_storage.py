import json
import os
from datetime import datetime

ACCOUNT_FILE = "accounts.json"

# 初始化文件
if not os.path.exists(ACCOUNT_FILE):
    with open(ACCOUNT_FILE, "w") as f:
        json.dump({}, f)

# 保存账号信息
def save_account(user_id: int, username: str, password: str):
    with open(ACCOUNT_FILE, "r") as f:
        data = json.load(f)

    data[str(user_id)] = {
        "username": username,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(ACCOUNT_FILE, "w") as f:
        json.dump(data, f, indent=2)

# 查询账号信息
def get_account(user_id: int):
    with open(ACCOUNT_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id))

# 检查是否已注册
def is_registered(user_id: int):
    return get_account(user_id) is not None

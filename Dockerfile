# 使用你想要的 Python 版本（如 3.11）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制文件
COPY . /app

# 安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 启动命令
CMD ["python", "jilibot.py"]

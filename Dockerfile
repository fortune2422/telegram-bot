# 使用 Python 3.11 的轻量镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目所有文件
COPY . /app

# 安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 启动命令
CMD ["python", "jilibot.py"]

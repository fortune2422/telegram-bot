# 使用 Python 3.11 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制代码和依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 默认端口（Render 会通过 PORT 环境变量传递）
ENV PORT=8443

# 启动命令
CMD ["python", "jilibot.py"]

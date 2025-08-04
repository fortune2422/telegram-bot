# 使用 Python 3.11 基础镜像
FROM python:3.11-slim

# 避免交互提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装 Playwright 所需系统依赖
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libxcomposite1 libxdamage1 libxrandr2 libxss1 libxtst6 \
    xdg-utils libgbm1 libgtk-3-0 \
 && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright 浏览器（Chromium）
RUN python -m playwright install --with-deps

# 复制项目文件
COPY . .

# Render 会提供 PORT 环境变量
ENV PORT=8443

# 启动命令
CMD ["python", "jilibot.py"]

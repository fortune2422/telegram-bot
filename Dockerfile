# 使用 Python 3.11 基础镜像
FROM python:3.11-slim

# 避免交互提示
ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 复制项目文件
COPY . .

# Render 会提供 PORT 环境变量
ENV PORT=8443

# 启动命令
CMD ["python", "jilibot.py"]

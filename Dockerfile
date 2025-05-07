# 1. 基础镜像
FROM python:3.11-slim

# 2. 安装编译工具和 Manim 运行时依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive-latex-base \
    texlive-latex-extra \
    fonts-noto \
    fonts-noto-cjk \
    librsvg2-bin \
    libpangocairo-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

# 3. 切换工作目录
WORKDIR /app

# 4. 复制代码
COPY . .

# 5. 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 6. 暴露端口
EXPOSE 5000

# 7. 启动命令
CMD ["python", "app.py"]

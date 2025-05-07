# 1. 选用官方 Python 轻量镜像
FROM python:3.11-slim

# 2. 安装系统依赖：FFmpeg（视频合并）、LaTeX（如果需要 Tex）、字体与 SVG 渲染库
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-latex-base \
    fonts-noto \
    fonts-noto-cjk \
    librsvg2 \
    libpangocairo-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

# 3. 设置工作目录
WORKDIR /app

# 4. 复制项目文件到容器
COPY . .

# 5. 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 6. 暴露 5000 端口（Flask 默认）
EXPOSE 5000

# 7. 启动命令
CMD ["python", "app.py"]

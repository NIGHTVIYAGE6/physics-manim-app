FROM python:3.11-slim

# 安装编译工具 & Manim 运行时依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive-latex-base \
    fonts-noto \
    fonts-noto-cjk \
    librsvg2-bin \
    libpangocairo-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]

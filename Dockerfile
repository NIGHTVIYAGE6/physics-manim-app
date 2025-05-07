RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive-latex-base \
    texlive-latex-extra \        # ← 增加这一行
    fonts-noto \
    fonts-noto-cjk \
    librsvg2-bin \
    libpangocairo-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

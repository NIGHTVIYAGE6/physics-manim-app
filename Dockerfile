FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
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


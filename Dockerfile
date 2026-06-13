FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    vim \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    cron \
    postgresql-client \
    gettext \
    netcat-openbsd \
    curl \
    unzip \
    zstd \
    ca-certificates && \
    apt-get clean

ENV OLLAMA_SKIP_CUDA_LIBS=1
# Instalar Ollama manualmente
RUN curl -fsSL https://ollama.com/install.sh | sh

# Crear directorio de trabajo
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pip-tools

COPY . /app

# Exponer puerto de Django y Ollama (si quieres acceder desde fuera)
EXPOSE 8000
EXPOSE 11434

# Comando que lanza Ollama en background y luego Django
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# RUN ollama pull mxbai-embed-large


CMD ["/app/start.sh"]

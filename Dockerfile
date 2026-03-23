# Azure Voice Language Lab - Dockerfile
# =====================================
#
# Imagem Docker para executar o Azure Voice Language Lab

FROM python:3.11-slim

# Metadados
LABEL maintainer="Rone Bragaglia <ronbragaglia@gmail.com>"
LABEL description="Azure Voice Language Lab - Toolkit para Azure Speech e Language Services"
LABEL version="1.1.0"

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Criar diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    portaudio19-dev \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY pyproject.toml setup.py ./
COPY requirements.txt ./

# Instalar dependências Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e ".[web,audio,visualization]"

# Copiar código fonte
COPY src/ ./src/
COPY web/ ./web/
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY README.md CHANGELOG.md LICENSE ./

# Criar diretórios necessários
RUN mkdir -p /app/output /app/audio_samples /app/logs

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 -s /bin/bash appuser && \
    chown -R appuser:appuser /app

# Trocar para usuário não-root
USER appuser

# Expor porta do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1

# Comando padrão
CMD ["streamlit", "run", "web/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

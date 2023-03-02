# app/Dockerfile

FROM python:3.10-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev\
    g++ \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry


COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry --version
RUN poetry config installer.modern-installation false
RUN poetry  install --no-interaction --no-ansi --no-root

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
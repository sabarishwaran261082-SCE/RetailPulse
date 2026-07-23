FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    useradd -m appuser

# Copy application
COPY --chown=appuser:appuser streamlit_app/ ./streamlit_app/

# Copy root project files
COPY --chown=root:root --chmod=0444 *.py ./
COPY --chown=appuser:appuser *.txt ./
COPY --chown=appuser:appuser *.yml ./
COPY --chown=appuser:appuser *.yaml ./

# Copy ONLY the processed dataset
COPY --chown=appuser:appuser data/processed/ ./data/processed/

# Copy models and reports
COPY --chown=appuser:appuser models/ ./models/
COPY --chown=appuser:appuser reports/ ./reports/

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
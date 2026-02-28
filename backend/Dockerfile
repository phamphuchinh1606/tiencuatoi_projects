# ═══════════════════════════════════════════════════════════════════════════════
# Dockerfile — DEVELOPMENT
# ———————————————————————————————————————————————————————————————————————————————
# Đặc điểm:
#   - Single stage (nhanh build, không tối ưu image size)
#   - Cài đầy đủ cả dev dependencies (pytest, ruff, mypy...)
#   - Uvicorn chạy với --reload → tự restart khi code thay đổi
#   - Source code mount qua volume trong docker-compose.yml
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.12-slim

WORKDIR /app

# Cài system dependencies cần cho build một số Python package
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài Poetry
RUN pip install --no-cache-dir poetry==1.8.4

# Copy file dependency trước để tận dụng Docker layer cache
COPY pyproject.toml poetry.lock* ./

# Cài tất cả dependencies (bao gồm dev) vào system Python
# virtualenvs.create false → không tạo venv riêng trong container
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy source code
# (sẽ bị override bởi volume mount ".:/app" trong docker-compose.yml)
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Hot-reload: theo dõi thay đổi trong thư mục app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "app"]

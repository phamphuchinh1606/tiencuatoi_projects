# 🚀 TienCuaToi — Backend API

Backend RESTful API xây dựng bằng **FastAPI**, **SQLAlchemy Async** và **MySQL**, tổ chức theo kiến trúc phân tầng (Layered Architecture) với Repository Pattern.

---

## 📦 Tech Stack

| Thành phần         | Công nghệ                              |
| ------------------ | -------------------------------------- |
| Framework          | FastAPI 0.115+                         |
| ORM                | SQLAlchemy 2.0 (Async)                 |
| Database           | MySQL (latest) + aiomysql              |
| Migrations         | Alembic                                |
| Validation         | Pydantic v2                            |
| Authentication     | JWT (python-jose) + bcrypt             |
| Package Manager    | Poetry                                 |
| Testing            | pytest-asyncio + httpx                 |
| Linter / Formatter | Ruff                                   |
| Containerization   | Docker + Docker Compose                |

---

## 🗂 Cấu trúc Project

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py        # get_current_user, CurrentUser...
│   │   └── v1/api_router.py       # Gom tất cả feature routers
│   ├── features/                  # Logic nghiệp vụ theo tính năng
│   │   ├── auth/                  # Đăng ký, đăng nhập
│   │   ├── users/                 # Quản lý người dùng
│   │   ├── products/              # Quản lý sản phẩm
│   │   └── orders/                # Quản lý đơn hàng
│   │       ├── router.py
│   │       ├── dependencies.py
│   │       ├── exceptions.py
│   │       ├── services/
│   │       └── schemas/
│   ├── models/                    # SQLAlchemy models (schema CSDL)
│   ├── repositories/              # Tầng truy cập DB
│   │   ├── interfaces/            # ABC contracts
│   │   └── implementations/      # Implement thực tế
│   ├── core/                      # Config, Security, Exceptions, Middleware
│   ├── db/                        # SQLAlchemy session & alembic base
│   ├── tasks/                     # Celery background jobs
│   ├── utils/                     # Helper functions
│   ├── constants/                 # Enums, messages
│   └── main.py                    # FastAPI app entry point
├── tests/                         # Cấu trúc mirror app/
│   ├── conftest.py
│   ├── features/
│   └── repositories/
├── alembic/                       # Database migrations
├── scripts/                       # One-time scripts (seed, admin)
├── docker/
│   └── mysql/init/                # SQL chạy lần đầu khi MySQL khởi tạo
├── Dockerfile                     # ← DEV: single-stage, hot-reload
├── Dockerfile.prod                # ← PROD: multi-stage, optimized
├── docker-compose.yml             # Orchestrate MySQL + phpMyAdmin + API
├── .env                           # Biến môi trường
├── pyproject.toml                 # Poetry dependencies
└── alembic.ini
```

---

## 🐳 Chạy bằng Docker (Khuyên dùng)

### Yêu cầu

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2+

Kiểm tra:

```bash
docker --version
docker compose version
```

---

### ⚡ Khởi động nhanh

**Bước 1 — Clone và vào thư mục project:**

```bash
git clone <repo-url>
cd backend
```

**Bước 2 — Kiểm tra file `.env`** (đã có sẵn, chỉnh nếu cần):

```bash
# Mặc định đã cấu hình phù hợp với Docker:
# MYSQL_ROOT_PASSWORD=rootpassword
# MYSQL_USER=tiencuatoi_user
# MYSQL_PASSWORD=tiencuatoi_password
# MYSQL_DATABASE=tiencuatoi
```

**Bước 3 — Build và khởi động toàn bộ services:**

```bash
docker compose up --build
```

> Lần đầu sẽ mất vài phút để build image Python và pull MySQL/phpMyAdmin.

**Bước 4 — Chạy database migration** (mở terminal mới):

```bash
# Tạo migration từ models hiện tại
docker compose exec api alembic revision --autogenerate -m "init"

# Áp dụng migration vào DB
docker compose exec api alembic upgrade head
```

**Bước 5 — Tạo tài khoản Admin** (tùy chọn):

```bash
docker compose exec api python scripts/create_admin.py
```

---

### 🌐 Truy cập các Services

| Service          | URL                          | Mô tả                    |
| ---------------- | ---------------------------- | ------------------------ |
| **FastAPI**      | http://localhost:8000        | Backend API              |
| **Swagger UI**   | http://localhost:8000/docs   | Tài liệu API tương tác   |
| **ReDoc**        | http://localhost:8000/redoc  | Tài liệu API (ReDoc)     |
| **phpMyAdmin**   | http://localhost:8080        | Quản lý MySQL qua web    |
| **MySQL**        | localhost:3306               | Kết nối DB trực tiếp     |

**Đăng nhập phpMyAdmin:**
- Username: `root`
- Password: `rootpassword`

---

### 📋 Các lệnh Docker thường dùng

```bash
# ── Khởi động ──────────────────────────────────────────────────────────────

# Khởi động tất cả services (background)
docker compose up -d

# Build lại image (sau khi thay đổi Dockerfile hoặc pyproject.toml)
docker compose up --build

# Chỉ khởi động service cụ thể
docker compose up mysql phpmyadmin
docker compose up api

# ── Logs ───────────────────────────────────────────────────────────────────

# Xem log tất cả services
docker compose logs -f

# Xem log riêng API
docker compose logs -f api

# Xem log riêng MySQL
docker compose logs -f mysql

# ── Exec vào container ─────────────────────────────────────────────────────

# Chạy lệnh trong container API
docker compose exec api <command>

# Ví dụ: mở shell trong container
docker compose exec api bash

# Chạy pytest
docker compose exec api pytest -v

# Chạy Alembic
docker compose exec api alembic upgrade head
docker compose exec api alembic revision --autogenerate -m "ten_migration"
docker compose exec api alembic downgrade -1

# ── Dừng / Xóa ─────────────────────────────────────────────────────────────

# Dừng tất cả (giữ nguyên data)
docker compose down

# Dừng và XÓA TOÀN BỘ DỮ LIỆU MySQL (cẩn thận!)
docker compose down -v

# Xóa image đã build (để build lại từ đầu)
docker compose down --rmi local
```

---

### 🔄 Hot-reload khi code thay đổi

Khi đang chạy `docker compose up`, mọi thay đổi trong thư mục `app/` sẽ **tự động restart** server mà không cần chạy lại Docker. Đây là nhờ:

- Volume mount: `.:/app` trong `docker-compose.yml`
- Uvicorn flag: `--reload --reload-dir app`

---

### 🏗 Docker Files

| File              | Dùng khi nào       | Đặc điểm                                          |
| ----------------- | ------------------ | ------------------------------------------------- |
| `Dockerfile`      | **Development**    | Single-stage, đủ dev deps, hot-reload             |
| `Dockerfile.prod` | **Production**     | Multi-stage, chỉ prod deps, nhỏ gọn, 4 workers   |

**Build và chạy production image:**

```bash
# Build production image
docker build -f Dockerfile.prod -t tiencuatoi-api:prod .

# Chạy production container
docker run -p 8000:8000 \
  --env-file .env \
  -e DATABASE_URL="mysql+aiomysql://user:password@host:3306/tiencuatoi" \
  tiencuatoi-api:prod
```

---

## 💻 Chạy Local (không dùng Docker)

### Yêu cầu

- Python 3.12+
- MySQL 8.0+
- [Poetry](https://python-poetry.org/docs/#installation)

### Cài đặt

```bash
# Cài dependencies
poetry install

# Kích hoạt virtual environment
poetry shell
```

### Cấu hình

Chỉnh `DATABASE_URL` trong `.env` trỏ về MySQL local:

```env
DATABASE_URL="mysql+aiomysql://root:yourpassword@localhost:3306/tiencuatoi"
```

### Chạy migration

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Tạo admin

```bash
python scripts/create_admin.py
```

### Khởi động server

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Chạy Tests

```bash
# Với Docker
docker compose exec api pytest -v

# Local
pytest -v

# Với coverage report
pytest --cov=app --cov-report=html
```

---

## 🔐 Authentication Flow

```
POST /api/v1/auth/register  → Đăng ký tài khoản
POST /api/v1/auth/login     → Đăng nhập, nhận access_token + refresh_token
```

Dùng token trong các request tiếp theo:

```
Authorization: Bearer <access_token>
```

---

## 🏛 Kiến trúc & Design Patterns

| Pattern                  | Mô tả                                                              |
| ------------------------ | ------------------------------------------------------------------ |
| **Repository Pattern**   | Tách logic DB qua Interface → Implementation, dễ unit test        |
| **Dependency Injection** | FastAPI `Depends()` tiêm Service, Repository vào endpoint          |
| **Feature-based**        | Code nhóm theo tính năng, không theo loại file                     |
| **Global Exceptions**    | Tập trung xử lý lỗi tại `core/exceptions.py`                      |
| **Layered Architecture** | Router → Service → Repository → DB                                 |

---

## 📝 Environment Variables

| Biến                         | Mô tả                          | Default              |
| ---------------------------- | ------------------------------ | -------------------- |
| `DATABASE_URL`               | MySQL connection string        | (xem .env)           |
| `SECRET_KEY`                 | JWT signing key                | **Bắt buộc đổi!**   |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Thời gian sống access token    | `30`                 |
| `REFRESH_TOKEN_EXPIRE_DAYS`  | Thời gian sống refresh token   | `7`                  |
| `MYSQL_ROOT_PASSWORD`        | MySQL root password (Docker)   | `rootpassword`       |
| `MYSQL_USER`                 | MySQL app user (Docker)        | `tiencuatoi_user`    |
| `MYSQL_PASSWORD`             | MySQL app password (Docker)    | `tiencuatoi_password`|
| `MYSQL_DATABASE`             | Tên database (Docker)          | `tiencuatoi`         |
| `API_PORT`                   | Port API (Docker)              | `8000`               |
| `PHPMYADMIN_PORT`            | Port phpMyAdmin (Docker)       | `8080`               |
| `DEBUG`                      | Bật Swagger docs               | `true`               |

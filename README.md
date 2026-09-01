# EMMI Benchmark Monitoring Dashboard

**European Money Markets Institute (EMMI)**  
Mar 2023 – Jun 2024

A secure data processing and API integration platform for benchmark monitoring and reporting in financial markets.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python 3.12, Django 4.2, Django REST Framework |
| Frontend | React 18, Vite, Axios, Recharts |
| Database | PostgreSQL 16 |
| Auth | JWT (SimpleJWT) |
| Infra | Docker, Nginx |

## Quick Start — Docker (recommended)

```bash
# clone the repo
git clone https://github.com/VelpuriManikanta/Emmi.git
cd Emmi

# start all services
docker compose up -d

# run migrations
docker compose exec backend python manage.py migrate

# create superuser
docker compose exec backend python manage.py createsuperuser
```

- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000/api/
- **Swagger docs:** http://localhost:8000/api/docs/
- **Django admin:** http://localhost:8000/admin/

## Local Development

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# copy and configure env
cp .env.example .env

# start PostgreSQL locally, then:
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev       # http://localhost:3000 (proxies /api to :8000)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/token/` | Get JWT token |
| POST | `/api/auth/token/refresh/` | Refresh token |
| GET | `/api/auth/me/` | Current user |
| GET/POST | `/api/benchmarks/` | List/create benchmarks |
| GET/PUT/DELETE | `/api/benchmarks/<code>/` | Benchmark detail |
| GET | `/api/benchmarks/types/` | Benchmark types |
| GET | `/api/benchmarks/analytics/` | Dashboard analytics |
| GET/POST | `/api/benchmarks/<code>/rates/` | List/create rates |
| GET/POST | `/api/reports/` | List/create reports |
| POST | `/api/reports/<id>/generate/` | Generate report |
| GET | `/api/reports/<id>/export/` | Export CSV |
| GET/POST | `/api/reports/schedules/` | Report schedules |
| GET | `/api/schema/` | OpenAPI schema |
| GET | `/api/docs/` | Swagger UI |

## Running Tests

```bash
# Backend
cd backend
pip install pytest pytest-django
python -m pytest

# Frontend lint
cd frontend
npm run lint
npm run build
```

## Project Structure

```
Emmi/
├── backend/
│   ├── config/          # Django settings, URLs, WSGI
│   ├── benchmarks/      # Benchmark models, API, validation
│   ├── reports/         # Reporting models, generation, export
│   ├── authentication/  # User auth, JWT
│   ├── api_tests.py     # API endpoint tests
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/         # Axios client + endpoint wrappers
│   │   ├── components/  # Layout shell
│   │   ├── context/     # Auth, Toast providers
│   │   └── pages/       # Dashboard, Benchmarks, Reports, Login
│   ├── vite.config.js
│   └── package.json
├── specs/               # Development methodology, tool specs
├── docker-compose.yml
└── README.md
```

## License

Private — European Money Markets Institute

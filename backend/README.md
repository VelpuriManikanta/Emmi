# Backend - Django REST Framework

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── config/           # Django settings
├── api/             # REST API endpoints
├── benchmarks/      # Benchmark data models
├── reports/         # Reporting module
└── authentication/  # Auth handlers
```

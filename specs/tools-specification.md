# Tools Specification

## Development Environment

### Backend Stack

```yaml
python:
  version: "3.10+"
  packages:
    - django==4.2.*
    - djangorestframework==3.14.*
    - psycopg2-binary==2.9.*
    - python-decouple==3.8.*
    - celery==5.3.*
    - redis==5.0.*

database:
  engine: postgresql
  version: "14+"
  features:
    - jsonb support
    - full text search
    - materialized views
```

### Frontend Stack

```yaml
react:
  version: "18+"
  packages:
    - react-router-dom
    - axios
    - chart.js or recharts
    - material-ui or tailwindcss

build:
  tool: vite or create-react-app
  linting: eslint
  formatting: prettier
```

## Tool Configurations

### Git Configuration

```gitconfig
[core]
    editor = code --wait
    
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --oneline --graph --decorate
    
[push]
    default = current
    autoSetupRemote = true
    
[pull]
    rebase = true
```

### VS Code Settings

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  }
}
```

### ESLint Configuration

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': 'warn',
  },
};
```

### Python Linting (pyproject.toml)

```toml
[tool.black]
line-length = 88
target-version = ['py310']

[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

## API Testing Tools

### Postman Collection

```json
{
  "info": {
    "name": "EMMI Dashboard API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8000/api"
    }
  ]
}
```

### curl Examples

```bash
# Authentication
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Get benchmarks
curl -X GET http://localhost:8000/api/benchmarks/ \
  -H "Authorization: Bearer <token>"
```

## Deployment Tools

### Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: emmi_dashboard
      POSTGRES_USER: emmi_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - web

volumes:
  postgres_data:
```

### GitHub Actions CI/CD

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          pytest
          
      - name: Run linting
        run: |
          flake8 .
          black --check .
```

## Monitoring Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| Sentry | Error tracking | Django integration |
| Prometheus | Metrics | Custom exporters |
| Grafana | Dashboards | Prometheus datasource |
| New Relic | APM | Python agent |

## Documentation Tools

| Tool | Purpose |
|------|---------|
| Swagger/OpenAPI | API documentation |
| MkDocs | Project documentation |
| Sphinx | Python docstrings |

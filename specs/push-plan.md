# 7-Day Push Plan

## Day 1 (Tomorrow) - Backend Foundation
```
feat: Django project setup with settings and URLs
- Initialize Django project
- Configure PostgreSQL database
- Setup REST framework
- Create base settings.py
```

## Day 2 - Database Models
```
feat: benchmark data models and migrations
- Benchmark model (name, value, date, source)
- Report model (title, generated_at, data)
- User profile model
- Create and run migrations
```

## Day 3 - Authentication API
```
feat: user authentication endpoints
- Login/logout API
- JWT token generation
- User registration endpoint
- Password reset flow
```

## Day 4 - Benchmark CRUD API
```
feat: benchmark CRUD REST endpoints
- GET/POST/PUT/DELETE /api/benchmarks/
- Pagination and filtering
- Data validation serializers
- Custom permissions
```

## Day 5 - Reporting API
```
feat: reporting and analytics endpoints
- GET /api/reports/
- POST /api/reports/generate/
- Aggregation queries
- Export functionality (CSV/JSON)
```

## Day 6 - Frontend Setup
```
feat: React project initialization
- Create React app with Vite
- Setup routing (react-router)
- Axios configuration
- Basic component structure
```

## Day 7 - Frontend-Backend Integration
```
feat: API integration and data flow
- Login page with auth
- Benchmark list dashboard
- Data visualization (charts)
- Error handling and loading states
```

## Commit Convention
```
feat:     new feature
fix:      bug fix
docs:     documentation
test:     adding tests
refactor: code improvement
```

## Daily Steps
1. `git checkout main`
2. `git pull origin main`
3. `git checkout -b feature/day-X-name`
4. Make changes
5. `git add .`
6. `git commit -m "feat: description"`
7. `git push origin feature/day-X-name`
8. Create PR and merge

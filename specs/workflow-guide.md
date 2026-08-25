# Development Workflow Guide

## Daily Push Protocol

### Commit Convention

```
[type]: short description (max 50 chars)

Types:
- feat:     New feature
- fix:      Bug fix
- docs:     Documentation changes
- style:    Code style changes (formatting, no logic change)
- refactor: Code refactoring
- test:     Adding/fixing tests
- chore:    Build process, dependencies, etc.
```

### Daily Checklist

1. [ ] Pull latest changes: `git pull origin main`
2. [ ] Create feature branch: `git checkout -b feature/description`
3. [ ] Make changes
4. [ ] Run tests: `pytest`
5. [ ] Run linting: `flake8 . && black --check .`
6. [ ] Stage changes: `git add .`
7. [ ] Commit: `git commit -m "feat: description"`
8. [ ] Push: `git push origin feature/description`
9. [ ] Create PR on GitHub

## Weekly Milestones

### Week 1: Foundation
- [ ] Project setup complete
- [ ] Database schema designed
- [ ] API skeleton created
- [ ] Authentication system

### Week 2: Backend Core
- [ ] Benchmark data models
- [ ] REST API endpoints
- [ ] Data validation logic
- [ ] Business logic layer

### Week 3: Frontend Foundation
- [ ] React project setup
- [ ] Component library
- [ ] Routing configuration
- [ ] API integration

### Week 4: Integration
- [ ] Frontend-backend integration
- [ ] Real-time data updates
- [ ] Error handling
- [ ] Loading states

### Week 5: Testing & QA
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] SIT environment setup
- [ ] QA feedback incorporation

### Week 6: Performance
- [ ] Database optimization
- [ ] API response time <200ms
- [ ] Frontend bundle optimization
- [ ] Caching implementation

### Week 7: Security
- [ ] Security audit
- [ ] Penetration testing
- [ ] Data encryption
- [ ] Compliance review

### Week 8: Deployment
- [ ] UAT environment
- [ ] Deployment scripts
- [ ] Monitoring setup
- [ ] Documentation finalization

## Git Commands Reference

```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/weekly-task

# Save progress (end of day)
git add .
git commit -m "feat: daily progress update"
git push origin feature/weekly-task

# Create PR
gh pr create --title "Week X: Feature Name" --body "Description"

# Merge (after review)
git checkout main
git merge feature/weekly-task
git push origin main
```

## Branch Strategy

```
main (production)
  └── develop (integration)
       ├── feature/week-1-setup
       ├── feature/week-2-backend
       ├── fix/issue-description
       └── ...
```

# Tools & Spec-Driven Development

## Overview

This document defines the development methodology, tools, and specifications for the EMMI Benchmark Monitoring Dashboard project.

## Development Methodology

### Spec-Driven Development (SDD)

1. **Write spec first** - Define requirements before code
2. **Implement to spec** - Code must match specification
3. **Test against spec** - Verify implementation meets requirements
4. **Update spec** - Revise specs when requirements change

### Weekly Cadence

| Week | Deliverable | Status |
|------|-------------|--------|
| 1 | Project setup, DB schema, API skeleton | |
| 2 | Backend services, authentication | |
| 3 | Frontend components, data visualization | |
| 4 | Integration testing, bug fixes | |
| 5 | UAT preparation, documentation | |
| 6 | Performance optimization | |
| 7 | Security review, compliance | |
| 8 | Final testing, deployment prep | |

### Daily Push Protocol

- **Commit message format**: `[type]: description`
  - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
- **Push time**: End of workday
- **Branch naming**: `feature/description`, `fix/description`

## Tools

### Backend Development

| Tool | Purpose | Version |
|------|---------|---------|
| Python | Primary language | 3.10+ |
| Django | Web framework | 4.2+ |
| Django REST Framework | API development | 3.14+ |
| PostgreSQL | Database | 14+ |
| psycopg2 | DB adapter | 2.9+ |

### Frontend Development

| Tool | Purpose | Version |
|------|---------|---------|
| React | UI framework | 18+ |
| JavaScript | Primary language | ES2022+ |
| HTML/CSS | Markup/Styling | HTML5/CSS3 |
| Axios | HTTP client | 1.6+ |

### Development Tools

| Tool | Purpose |
|------|---------|
| Git | Version control |
| VS Code | IDE |
| Postman | API testing |
| Docker | Containerization |
| GitHub Actions | CI/CD |

### Testing Tools

| Tool | Purpose |
|------|---------|
| pytest | Python testing |
| Jest | JavaScript testing |
| Selenium | E2E testing |

## Specifications

### API Specification

- RESTful design principles
- JSON response format
- OAuth2 authentication
- Rate limiting: 100 requests/minute

### Database Schema

- Normalized relational design
- Indexes on frequently queried fields
- Soft deletes for audit trail

### Code Standards

- PEP 8 for Python
- ESLint for JavaScript
- Type hints required
- Docstrings for public methods

### Security Requirements

- HTTPS only
- JWT token authentication
- Input validation on all endpoints
- SQL injection prevention
- XSS protection

## Workflow

```
1. Create feature branch
2. Write/update specification
3. Implement changes
4. Write tests
5. Run linting and type checks
6. Create PR with spec reference
7. Code review
8. Merge to main
9. Daily push to remote
```

## Tracking

- Use GitHub Issues for task tracking
- Link commits to issues
- Weekly milestone reviews
- Daily standup notes in PR descriptions

# Frontend - React + Vite

## Setup

```bash
npm install
npm run dev       # starts Vite dev server on :3000 (proxies /api to :8000)
npm run build     # production build to dist/
npm run lint      # eslint check
```

## Pages

| Route | Description |
|-------|-------------|
| `/login` | Sign in with JWT |
| `/dashboard` | Analytics overview |
| `/benchmarks` | Benchmark list with search |
| `/benchmarks/:code` | Benchmark detail + rate history |
| `/reports` | Report list, generate, CSV export |

## Structure

```
frontend/
├── src/
│   ├── api/           # Axios client + endpoint wrappers
│   ├── components/    # Layout shell
│   ├── context/       # Auth context
│   ├── pages/         # Route pages
│   ├── App.jsx        # Routing + auth guard
│   ├── main.jsx       # Entry point
│   └── styles.css     # Global styles
├── index.html
├── vite.config.js     # Dev proxy to Django backend
└── package.json
```
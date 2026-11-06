# TaskFlow

TaskFlow is a Todo Management Web Application. Users can create an account, sign in, manage their own Todos, view dashboard statistics, and sign out.

## Features

- User signup, signin, current-user lookup, and logout.
- Argon2 password hashing.
- JWT authentication in an HttpOnly cookie.
- CSRF token cookie/header protection and Origin validation for state-changing requests.
- Todo creation, listing, retrieval, editing, deletion, completion, and pending status.
- User-scoped Todo access and dashboard statistics.
- Responsive HTML/Tailwind CSS/Vanilla JavaScript frontend.
- Docker Compose deployment with FastAPI, Nginx, and MongoDB.

## Technology stack

- Python 3.12
- FastAPI 0.115.6 and Uvicorn 0.34.0
- PyMongo 4.10.1
- Pydantic Settings 2.7.1
- PyJWT 2.10.1
- pwdlib with Argon2
- MongoDB 7.0
- HTML and Vanilla JavaScript
- Tailwind CSS 4.3.4 with `@tailwindcss/cli`
- Nginx 1.27-alpine
- Docker Compose
- Pytest 8.3.4

## System architecture

```text
Browser
  |
  | http://localhost:8080
  v
Nginx frontend
  |-- static HTML, CSS, and JavaScript
  `-- /api/* reverse proxy --> FastAPI backend :8000
                                      |
                                      v
                                  MongoDB
```

The backend exposes port 8000 in the current Compose configuration. MongoDB has no host port mapping and is reachable by the services through the Compose network.

## Project structure

```text
taskflow/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── src/css/input.css
│   ├── src/js/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── nginx.conf
│   └── Dockerfile
├── docs/
│   ├── prompts/PROMPT_LOG.md
│   └── qa/backend-qa-report.md
├── presentation/
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Prerequisites

- Docker Engine with Docker Compose v2.
- For host-side backend tests: Python 3.12+, `pip`, and a reachable MongoDB instance.
- For host-side frontend builds: Node.js and npm.

Docker is sufficient to run the application.

## Installation and configuration

```bash
cp .env.example .env
```

Edit `.env` before using the application outside local development. In particular, replace the placeholder `JWT_SECRET_KEY` with a strong secret and review cookie and Origin settings. `.env` is ignored by Git; `.env.example` contains placeholders only.

## Docker startup and shutdown

Start all services:

```bash
docker compose up --build
```

Start in the background:

```bash
docker compose up --build -d
```

Check service health:

```bash
docker compose ps
```

Stop and remove containers and networks:

```bash
docker compose down
```

MongoDB data is stored in the named `mongo_data` volume. To remove that data explicitly:

```bash
docker compose down -v
```

## Application URLs

- Frontend: <http://localhost:8080>
- Login: <http://localhost:8080/login>
- Signup: <http://localhost:8080/signup>
- Dashboard: <http://localhost:8080/dashboard>
- Backend health: <http://localhost:8000/api/health>
- Swagger UI: <http://localhost:8000/docs>
- OpenAPI JSON: <http://localhost:8000/openapi.json>

## Environment variables

| Variable | Purpose | Example |
|---|---|---|
| `APP_ENV` | Runtime environment label | `development` |
| `APP_HOST` | Uvicorn bind host | `0.0.0.0` |
| `APP_PORT` | Backend port | `8000` |
| `MONGODB_URI` | MongoDB connection URI | `mongodb://mongodb:27017` |
| `MONGODB_DATABASE` | Database name | `taskflow` |
| `JWT_SECRET_KEY` | JWT signing secret | Replace placeholder |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRE_MINUTES` | JWT lifetime | `30` |
| `AUTH_COOKIE_NAME` | HttpOnly auth cookie name | `taskflow_auth` |
| `CSRF_COOKIE_NAME` | CSRF cookie name | `taskflow_csrf` |
| `COOKIE_SECURE` | Secure-cookie flag | `false` locally |
| `COOKIE_SAMESITE` | SameSite cookie policy | `lax` |
| `ALLOWED_ORIGINS` | Comma-separated allowed Origins | `http://localhost:8000,http://localhost:8080` |
| `FRONTEND_PORT` | Published frontend port | `8080` |
| `LOG_LEVEL` | Application log level | `INFO` |

These are the variables defined in `.env.example` and consumed by the application or Compose configuration.

## API endpoints

State-changing requests require an allowed `Origin`. Authenticated state-changing requests also require the `X-CSRF-Token` header matching the readable CSRF cookie.

### Health

| Method | Path | Auth |
|---|---|---|
| `GET` | `/api/health` | None |

### Authentication

| Method | Path | Auth |
|---|---|---|
| `POST` | `/api/auth/signup` | Origin |
| `POST` | `/api/auth/signin` | Origin |
| `POST` | `/api/auth/logout` | JWT cookie + Origin + CSRF |
| `GET` | `/api/auth/me` | JWT cookie |

Signup expects `name`, `email`, and `password`. Signin expects `email` and `password`.

### Todos

| Method | Path | Auth |
|---|---|---|
| `POST` | `/api/todos` | JWT cookie + Origin + CSRF |
| `GET` | `/api/todos` | JWT cookie |
| `GET` | `/api/todos/{todo_id}` | JWT cookie |
| `PUT` | `/api/todos/{todo_id}` | JWT cookie + Origin + CSRF |
| `DELETE` | `/api/todos/{todo_id}` | JWT cookie + Origin + CSRF |
| `PATCH` | `/api/todos/{todo_id}/complete` | JWT cookie + Origin + CSRF |
| `PATCH` | `/api/todos/{todo_id}/pending` | JWT cookie + Origin + CSRF |
| `PATCH` | `/api/todos/{todo_id}/uncomplete` | JWT cookie + Origin + CSRF |

Todo create/update expects `title` and an optional `description`.

### Dashboard

| Method | Path | Auth |
|---|---|---|
| `GET` | `/api/dashboard/stats` | JWT cookie |

The response contains `total`, `completed`, and `pending` counts for the authenticated user.

## Database architecture

MongoDB uses two collections:

- `users`: UUID-string `_id`, name, unique email, Argon2 `password_hash`, and `created_at`.
- `todos`: UUID-string `_id`, `user_id`, title, description, completed flag, `created_at`, and `updated_at`.

Indexes created at startup:

- Unique `users.email`.
- Compound `todos.user_id + created_at`.
- Compound `todos.user_id + completed`.

Every Todo repository operation filters by both Todo ID and authenticated user ID.

## Authentication

The backend signs JWT access tokens with the configured secret and stores them in an HttpOnly cookie. The frontend uses `credentials: "include"` and never stores authentication tokens or passwords in browser storage.

Signin issues a readable CSRF cookie for authenticated state-changing requests. State-changing requests validate the request Origin, and authenticated operations additionally validate the `X-CSRF-Token` header using constant-time comparison.

## Testing

Run the backend tests with an installed virtual environment:

```bash
PYTHONPATH=backend .venv/bin/pytest -q backend/tests
```

The suite uses a uniquely named `taskflow_test_<uuid>` MongoDB database and drops it during session teardown. It should not be pointed at a development database.

To run the tests using the production backend image while mounting tests read-only and using the Compose MongoDB service:

```bash
MONGODB_URI=mongodb://mongodb:27017 docker compose run --rm \
  -e PYTHONPATH=/app \
  -e MONGODB_URI=mongodb://mongodb:27017 \
  -v "$PWD/backend/tests:/tmp/taskflow-tests:ro" \
  backend \
  pytest -q -p no:cacheprovider /tmp/taskflow-tests
```

Build the frontend CSS locally:

```bash
cd frontend
npm ci
npm run build:css
```

The generated `frontend/public/styles.css` is ignored because the Docker build generates it from the pinned dependencies.

## Screenshots

No screenshots are currently committed to this repository. The live UI can be viewed at the frontend URLs above after starting Compose.

## Troubleshooting

- **Frontend cannot reach the API:** confirm all services are healthy with `docker compose ps`, and use the frontend URL so requests go through Nginx `/api` proxying.
- **Backend fails during startup:** verify `MONGODB_URI`, `MONGODB_DATABASE`, and that the MongoDB service is healthy.
- **JWT configuration error:** `JWT_SECRET_KEY` must be at least 32 characters and should be replaced before non-development use.
- **403 on signup or signin:** send an `Origin` listed in `ALLOWED_ORIGINS`.
- **403 on Todo mutations or logout:** send the readable CSRF cookie value in `X-CSRF-Token`.
- **Port conflict:** change `FRONTEND_PORT` or `APP_PORT` in `.env`, then recreate the Compose services.
- **Stale database data:** `docker compose down -v` removes the named MongoDB volume; use this only when intentionally discarding local data.

## Security considerations

- Never commit `.env`, JWT secrets, passwords, or MongoDB credentials.
- Use a strong random `JWT_SECRET_KEY`.
- Set `COOKIE_SECURE=true` when serving over HTTPS.
- Restrict `ALLOWED_ORIGINS` to trusted origins.
- Keep MongoDB unexposed to the host.
- Keep the backend and dependencies updated and run the test suite before changes are released.
- Do not expose `password_hash` in API responses.

## Future improvements

Potential improvements not currently implemented include password reset and email verification, rate limiting, production MongoDB authentication and TLS, richer audit logging, automated browser tests, and committed deployment infrastructure.

## Project information

**Project:** TaskFlow Todo Management Web Application  
**Repository:** This TaskFlow repository  
**Author:** Not specified in the repository  
**License:** Not specified in the repository

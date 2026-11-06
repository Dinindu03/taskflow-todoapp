# TaskFlow AI Development Prompt History

This index organizes the prompt records available in [`PROMPT_LOG.md`](./PROMPT_LOG.md). The log is the canonical source for exact original wording; each record below links to its preserved prompt section and records only outputs verified in the repository.

## PROMPT-002 — Business Analyst Agent

- **Agent or role:** Senior Business Analyst using BMAD.
- **Development phase:** Discovery and business analysis.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-002](./PROMPT_LOG.md#prompt-002--business-analyst-agent)
- **Purpose:** Define the TaskFlow problem, users, requirements, constraints, scope, risks, assumptions, and acceptance criteria.
- **Actual output:** [`project-brief.md`](../../_bmad-output/planning-artifacts/project-brief.md); canonical prompt record in [`PROMPT_LOG.md`](./PROMPT_LOG.md).
- **Follow-up corrections:** No application code was requested or added.

## PROMPT-003 — Product Manager Agent

- **Agent or role:** Senior BMAD Product Manager.
- **Development phase:** Product requirements.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-003](./PROMPT_LOG.md#prompt-003--product-manager-agent)
- **Purpose:** Convert the approved brief into a traceable PRD with unique requirement and story IDs and testable acceptance criteria.
- **Actual output:** [`product-requirements-document.md`](../../_bmad-output/planning-artifacts/product-requirements-document.md).
- **Follow-up corrections:** No application code was requested or added.

## PROMPT-004 — Software Architect Agent

- **Agent or role:** Senior Software Architect.
- **Development phase:** System architecture.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-004](./PROMPT_LOG.md#prompt-004--software-architect-agent)
- **Purpose:** Design the maintainable FastAPI, MongoDB, frontend, authentication, Docker, API, validation, testing, and deployment architecture.
- **Actual output:** [`system-architecture.md`](../../_bmad-output/planning-artifacts/system-architecture.md).
- **Follow-up corrections:** Architecture specified UUID strings, ownership-scoped Todo operations, cookie JWTs, CSRF, and Origin protection.

## PROMPT-005 — Product Owner Review

- **Agent or role:** BMAD Product Owner.
- **Development phase:** Requirements and architecture review.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-005](./PROMPT_LOG.md#prompt-005--product-owner-review)
- **Purpose:** Identify missing, conflicting, or unsafe requirements before implementation.
- **Actual output:** [`product-owner-approval-report.md`](../../_bmad-output/planning-artifacts/product-owner-approval-report.md).
- **Follow-up corrections:** Report recorded conditional approval and 18 findings without silently changing approved requirements.

## PROMPT-006 — Scrum Master

- **Agent or role:** BMAD Scrum Master.
- **Development phase:** Implementation planning.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-006](./PROMPT_LOG.md#prompt-006--scrum-master)
- **Purpose:** Break the approved work into prioritized stories across nine implementation epics.
- **Actual output:** [`implementation-stories.md`](../../_bmad-output/planning-artifacts/implementation-stories.md).
- **Follow-up corrections:** Added a prerequisite contract-closure story and dependencies to the backlog.

## PROMPT-007 — UX/UI Designer

- **Agent or role:** Professional UI/UX Designer.
- **Development phase:** Experience and interface design.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-007](./PROMPT_LOG.md#prompt-007--uxui-designer)
- **Purpose:** Specify responsive, accessible screens and reusable components without changing the PRD.
- **Actual output:** [`ux-ui-specification.md`](../../_bmad-output/planning-artifacts/ux-ui-specification.md).
- **Follow-up corrections:** Approved PRD was not modified.

## PROMPT-008 — Project Infrastructure

- **Agent or role:** Senior Full-Stack Developer.
- **Development phase:** Project scaffolding.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-008](./PROMPT_LOG.md#prompt-008--project-infrastructure)
- **Purpose:** Create the modular frontend/backend directory structure and configuration skeleton.
- **Actual output:** Backend and frontend directories, Dockerfiles, Compose configuration, `.env.example`, `.gitignore`, README, and `presentation/`.
- **Follow-up corrections:** Added only the health shell and necessary configuration; feature implementation was deferred.

## PROMPT-009 — FastAPI Backend Setup

- **Agent or role:** FastAPI backend developer.
- **Development phase:** Backend foundation.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-009](./PROMPT_LOG.md#prompt-009--fastapi-backend-setup)
- **Purpose:** Add FastAPI, Uvicorn, Pydantic Settings, PyMongo, security dependencies, error handling, and `/api/health`.
- **Actual output:** [`backend/app/main.py`](../../backend/app/main.py), [`config.py`](../../backend/app/config.py), [`database.py`](../../backend/app/database.py), `requirements.txt`, and health test.
- **Follow-up corrections:** Used a project `.venv` because host pip was unavailable; verified the live health endpoint.

## PROMPT-010 — MongoDB Integration

- **Agent or role:** Backend database developer.
- **Development phase:** Persistence layer.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-010](./PROMPT_LOG.md#prompt-010--mongodb-integration)
- **Purpose:** Add users and todos collections, UUID IDs, indexes, connection validation, duplicate-email handling, and safe user responses.
- **Actual output:** Database initialization, document models, repositories, database tests, and MongoDB Compose integration.
- **Follow-up corrections:** Tests were run inside the Compose network after host MongoDB access was unavailable.

## PROMPT-011 — Authentication Development

- **Agent or role:** FastAPI authentication developer.
- **Development phase:** Authentication and authorization.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-011](./PROMPT_LOG.md#prompt-011--authentication-development)
- **Purpose:** Implement signup, signin, logout, current-user lookup, Argon2 hashing, JWT cookies, CSRF, and Origin protection.
- **Actual output:** [`security.py`](../../backend/app/security.py), auth schemas, service, routes, and auth tests.
- **Follow-up corrections:** Removed password hashes from responses, corrected invalid-credential status to 401, and corrected logout to 204.

## PROMPT-012 — Todo CRUD Development

- **Agent or role:** FastAPI Todo API developer.
- **Development phase:** Core task management.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-012](./PROMPT_LOG.md#prompt-012--todo-crud-development)
- **Purpose:** Implement authenticated Todo CRUD and completion-state operations with strict ownership filtering.
- **Actual output:** [`todos.py` route module](../../backend/app/routes/todos.py), Todo schemas/repository, and CRUD/isolation tests.
- **Follow-up corrections:** Added whitespace-only title validation and safe cross-user 404 behavior.

## PROMPT-013 — Dashboard Statistics

- **Agent or role:** FastAPI dashboard developer.
- **Development phase:** Dashboard backend.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-013](./PROMPT_LOG.md#prompt-013--dashboard-statistics)
- **Purpose:** Return authenticated-user-only total, completed, and pending counts.
- **Actual output:** Dashboard route/schema, repository aggregation, and multi-user/empty-user tests.
- **Follow-up corrections:** Verified zero-valued statistics for users without Todos.

## PROMPT-014 — Tailwind CSS Setup

- **Agent or role:** Frontend developer.
- **Development phase:** Frontend build tooling.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-014](./PROMPT_LOG.md#prompt-014--tailwind-css-setup)
- **Purpose:** Configure reproducible Tailwind CLI compilation without the CDN.
- **Actual output:** [`package.json`](../../frontend/package.json), lockfile, Tailwind input, generated-build configuration, and frontend multi-stage Docker build.
- **Follow-up corrections:** Pinned Tailwind and CLI to 4.3.4 after checking the registry; verified CSS output and Nginx serving.

## PROMPT-015 — Authentication UI

- **Agent or role:** Frontend developer.
- **Development phase:** Authentication interface.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-015](./PROMPT_LOG.md#prompt-015--authentication-ui)
- **Purpose:** Build responsive signup/signin forms with validation, feedback, password visibility, and cookie-based API calls.
- **Actual output:** [`index.html`](../../frontend/index.html), [`auth.js`](../../frontend/src/js/auth.js), and frontend Compose integration.
- **Follow-up corrections:** Signin redirects to the dashboard; no browser storage is used for passwords or tokens.

## PROMPT-016 — TaskFlow Dashboard

- **Agent or role:** Frontend developer.
- **Development phase:** Main application interface.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-016](./PROMPT_LOG.md#prompt-016--taskflow-dashboard)
- **Purpose:** Build the responsive dashboard and connect task operations, filters, statistics, and logout to the API.
- **Actual output:** [`dashboard.html`](../../frontend/dashboard.html) and [`dashboard.js`](../../frontend/src/js/dashboard.js).
- **Follow-up corrections:** Added credentialed CORS support and corrected local statistics to refresh from the backend.

## PROMPT-017 — Frontend and Backend Integration

- **Agent or role:** Full-stack integration developer.
- **Development phase:** End-to-end integration.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-017](./PROMPT_LOG.md#prompt-017--frontend-and-backend-integration)
- **Purpose:** Verify the complete user journey and correct relative API paths, credentials, response handling, and proxying.
- **Actual output:** [`nginx.conf`](../../frontend/nginx.conf), relative Fetch API calls, improved API error handling, and integration verification.
- **Follow-up corrections:** Replaced hard-coded `localhost:8000` calls with relative `/api` paths and added Nginx `/api` proxying.

## PROMPT-018 — Backend Dockerization

- **Agent or role:** Backend DevOps developer.
- **Development phase:** Backend container hardening.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-018](./PROMPT_LOG.md#prompt-018--backend-dockerization)
- **Purpose:** Produce a production-appropriate non-root FastAPI image with environment-driven Uvicorn and health checks.
- **Actual output:** [`backend/Dockerfile`](../../backend/Dockerfile).
- **Follow-up corrections:** Changed to a multi-stage image, removed runtime tests, added UID 10001, and verified the image health endpoint.

## PROMPT-019 — Frontend Dockerization

- **Agent or role:** Frontend DevOps developer.
- **Development phase:** Frontend containerization.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-019](./PROMPT_LOG.md#prompt-019--frontend-dockerization)
- **Purpose:** Build Tailwind assets in one stage and serve routed pages and proxied APIs from Nginx.
- **Actual output:** [`frontend/Dockerfile`](../../frontend/Dockerfile) and [`frontend/nginx.conf`](../../frontend/nginx.conf).
- **Follow-up corrections:** Added `/login`, `/signup`, `/dashboard` routes, frontend health checks, and fixed the Nginx document root.

## PROMPT-020 — Docker Compose Integration

- **Agent or role:** Docker Compose integration developer.
- **Development phase:** Local service orchestration.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-020](./PROMPT_LOG.md#prompt-020--docker-compose-integration)
- **Purpose:** Orchestrate frontend, backend, and MongoDB with persistent storage, dependencies, health checks, and network isolation.
- **Actual output:** [`docker-compose.yml`](../../docker-compose.yml) and `.env.example` updates.
- **Follow-up corrections:** Service names became `frontend`, `backend`, and `mongodb`; frontend uses public ingress plus internal API connectivity, while MongoDB remains unpublished.

## PROMPT-021 — Backend QA Agent

- **Agent or role:** Senior QA Engineer.
- **Development phase:** Backend verification.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-021](./PROMPT_LOG.md#prompt-021--backend-qa-agent)
- **Purpose:** Cover backend authentication, Todo, isolation, validation, missing-resource, and health behavior against an isolated database.
- **Actual output:** [`backend/tests/conftest.py`](../../backend/tests/conftest.py), expanded tests, and [`backend-qa-report.md`](../qa/backend-qa-report.md).
- **Follow-up corrections:** Added unique test database teardown; corrected expected Origin/CSRF behavior; final isolated suite passed 13 tests.

## PROMPT-022 — Security Review

- **Agent or role:** Security review role.
- **Development phase:** Security assessment.
- **Exact original prompt:** No PROMPT-022 record is present in the repository prompt log; no exact original wording is reproduced here.
- **Purpose:** Not recorded in the available repository history.
- **Actual output:** A security-review response exists in the interaction history, but no repository prompt record or security-review document was created.
- **Follow-up corrections:** None recorded in repository files.

## PROMPT-023 — Documentation Agent: Generate README

- **Agent or role:** Senior Technical Documentation Engineer.
- **Development phase:** Repository documentation.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-023](./PROMPT_LOG.md#prompt-023--documentation-agent-generate-readme)
- **Purpose:** Generate a complete README from the actual source, configuration, routes, tests, and Docker setup.
- **Actual output:** [`README.md`](../../README.md).
- **Follow-up corrections:** Documented actual backend port exposure, internal MongoDB, routes, environment variables, and test commands.

## PROMPT-024 — README Verification

- **Agent or role:** Independent Technical Reviewer.
- **Development phase:** Documentation verification.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-024](./PROMPT_LOG.md#prompt-024--readme-verification)
- **Purpose:** Compare README claims and commands against source code and safe runtime checks.
- **Actual output:** Corrected [`README.md`](../../README.md).
- **Follow-up corrections:** Corrected CSRF-cookie wording and made the Docker test command Compose-compatible.

## PROMPT-025 — Prompt History Documentation

- **Agent or role:** Technical Project Documentation Assistant.
- **Development phase:** Prompt-history organization.
- **Exact original prompt:** [`PROMPT_LOG.md` — PROMPT-025](./PROMPT_LOG.md#prompt-025--prompt-history-documentation)
- **Purpose:** Organize available prompt records with roles, phases, purposes, outputs, and corrections while preserving canonical wording.
- **Actual output:** This [`PROMPT_HISTORY.md`](./PROMPT_HISTORY.md) index and the exact prompt appended to [`PROMPT_LOG.md`](./PROMPT_LOG.md).
- **Follow-up corrections:** Explicitly marked PROMPT-022 as absent from the repository instead of fabricating its wording or execution record.

## Repository status

The workspace is not a Git repository, so no Git commit or GitHub push can be created from this environment. The organized history is saved locally in `docs/prompts/`; it can be committed after the repository is initialized or made available.

# TaskFlow MVP Implementation Stories

**Status:** Implementation backlog  
**Source artifacts:** Project Brief, PRD, System Architecture, Product Owner Approval Report  
**Priority:** `P0` = required for MVP, `P1` = MVP quality/release support  
**Dependency notation:** Story IDs identify prerequisites; dependencies are not implied by list order.

## Backlog Summary

| Epic | Stories | Priority |
|---|---|---|
| 1. Project infrastructure | INFRA-001, INFRA-002 | P0 |
| 2. Database setup | DB-001, DB-002 | P0 |
| 3. User authentication | AUTH-001, AUTH-002, AUTH-003, AUTH-004 | P0 |
| 4. Todo management | TODO-001, TODO-002, TODO-003 | P0 |
| 5. Frontend development | UI-001, UI-002, UI-003 | P0 |
| 6. Dashboard | DASH-001 | P0 |
| 7. Docker integration | DOCKER-001, DOCKER-002 | P0 |
| 8. Testing | TEST-001, TEST-002, TEST-003 | P0/P1 |
| 9. Documentation | DOC-001, DOC-002 | P1 |

## Cross-Cutting Definition of Done

Every implementation story is complete only when:

- The story's acceptance criteria pass.
- Validation and errors are explicit and safe.
- No password, token, password hash, or secret is returned or logged.
- Ownership checks are enforced server-side where user data is involved.
- Relevant automated tests or repeatable verification are added.
- Documentation affected by the story is updated.

## 0. Pre-Implementation Contract Closure

### STORY-000 — Resolve implementation contract decisions

**Story ID:** `STORY-000`  
**Priority:** P0  
**Description:** Resolve the Product Owner approval conditions before source implementation begins. The decisions must be recorded as implementation notes or updates to the approved API/test contract; no product scope expansion is authorized.

**Tasks**

- Select `email` or another canonical login identifier, including normalization and case rules.
- Select the MVP todo fields, including whether optional `description` is included.
- Define validation status code and stable error-envelope shape.
- Define signin response (cookies plus safe user/session metadata only) and logout semantics.
- Define CSRF generation, rotation, clearing, and Origin behavior.
- Define task-list ordering and bounded/paginated behavior.
- Define health/readiness semantics, index readiness behavior, and authentication rate-limit posture.
- Record decisions and map them to acceptance tests.

**Acceptance criteria**

- All PO-001 through PO-018 decisions marked resolved or explicitly deferred by the Product Owner.
- The API contract contains canonical auth, todo, dashboard, error, health, and list behavior.
- The test plan contains cases for CSRF, Origin, cookie security, ownership isolation, indexes, and idempotent status changes.
- No decision adds excluded MVP features without separate approval.

**Dependencies:** None.  
**Testing requirements:** Review checklist; contract consistency review across brief, PRD, architecture, and backlog.

## Epic 1: Project Infrastructure

### STORY-INFRA-001 — Establish maintainable FastAPI project structure

**Story ID:** `INFRA-001`  
**Priority:** P0  
**Description:** Create the application foundation with separate API/router, schema, security, service, repository, configuration, and static-asset boundaries.

**Tasks**

- Create the Python package and application entry point.
- Add configuration loading and fail-fast required-setting validation.
- Add dependency management and development tooling configuration.
- Establish router, schema, service, repository, and infrastructure module boundaries.
- Add application logging with secret/token redaction rules.
- Add a minimal `/health` route contract.

**Acceptance criteria**

- The FastAPI application imports and starts with valid configuration.
- Missing required configuration produces an explicit startup/configuration error.
- Routes, schemas, services, repositories, and infrastructure have separable module boundaries.
- `/health` returns the documented liveness/readiness shape without sensitive data.

**Dependencies:** `STORY-000`.  
**Testing requirements:** Import/startup smoke test; configuration validation tests; health endpoint test.

### STORY-INFRA-002 — Define shared API schemas and error contract

**Story ID:** `INFRA-002`  
**Priority:** P0  
**Description:** Establish consistent Pydantic request/response models, UUID string serialization, UTC timestamp serialization, and stable safe errors.

**Tasks**

- Define common error envelope and machine-readable error codes.
- Define user-safe response models that exclude `password_hash`.
- Define todo request/response models and field constraints.
- Define authentication, dashboard, pagination/list, and health response models.
- Register centralized validation and unexpected-error handlers.

**Acceptance criteria**

- Documented endpoints use the shared response and error shapes.
- Validation failures use the selected public status code consistently.
- Password hashes, tokens, and secrets cannot appear in response models.
- UUIDs serialize as strings and timestamps use the selected UTC format.

**Dependencies:** `STORY-000`, `INFRA-001`.  
**Testing requirements:** Schema validation tests; error-handler tests; response serialization tests.

## Epic 2: Database Setup

### STORY-DB-001 — Configure MongoDB client and users/todos repositories

**Story ID:** `DB-001`  
**Priority:** P0  
**Description:** Implement the infrastructure boundary for MongoDB and repository operations for the `users` and `todos` collections using string UUID document identifiers.

**Tasks**

- Configure one managed MongoDB client lifecycle.
- Implement user create/find operations using the canonical login identifier.
- Implement todo create/list/get/update/delete/status operations.
- Generate UUID strings in the application for `_id` and `user_id`.
- Ensure every todo repository method requires and filters by authenticated `user_id`.
- Prevent update operators from changing `_id` or `user_id`.

**Acceptance criteria**

- Users and todos persist in the specified collections with string UUID identifiers.
- Every todo read and mutation query includes the authenticated user ID.
- A caller cannot supply ownership to create or update a todo.
- Missing or inaccessible todos produce the selected safe response.

**Dependencies:** `STORY-000`, `INFRA-001`, `INFRA-002`.  
**Testing requirements:** Repository integration tests against an isolated MongoDB; cross-user isolation tests; UUID and update-field tests.

### STORY-DB-002 — Create and verify MongoDB indexes

**Story ID:** `DB-002`  
**Priority:** P0  
**Description:** Add repeatable index initialization and readiness verification for login uniqueness, task listing, and dashboard queries.

**Tasks**

- Create a unique index on the canonical user login field.
- Create compound todo indexes for `user_id` plus creation/order field and completion state.
- Make index creation idempotent.
- Verify required indexes before reporting database readiness.
- Define behavior when index creation fails.

**Acceptance criteria**

- Duplicate canonical login identifiers are rejected at the database boundary.
- Required indexes exist after initialization.
- Readiness does not report success when required indexes cannot be verified.
- Task list and dashboard repository queries use the intended indexed fields.

**Dependencies:** `STORY-000`, `DB-001`.  
**Testing requirements:** Index creation/verification integration tests; duplicate-key test; readiness failure test.

## Epic 3: User Authentication

### STORY-AUTH-001 — Implement secure signup

**Story ID:** `AUTH-001`  
**Priority:** P0  
**Description:** Allow a visitor to create an account using the selected canonical login identifier and password policy.

**Tasks**

- Validate and normalize signup input.
- Enforce the documented password policy.
- Hash passwords with Argon2id as the approved MVP standard.
- Handle duplicate identifiers safely.
- Return only the safe user response.

**Acceptance criteria**

- Valid signup creates one user with a string UUID and password hash.
- Plaintext password is never persisted, returned, or logged.
- Invalid input creates no account and returns field-safe validation errors.
- Duplicate normalized identifiers return the selected conflict response without leaking sensitive details.

**Dependencies:** `STORY-000`, `INFRA-002`, `DB-001`, `DB-002`.  
**Testing requirements:** Unit tests for hashing/validation; API tests for valid, invalid, duplicate, and secret-redaction cases.

### STORY-AUTH-002 — Implement signin and secure cookie session

**Story ID:** `AUTH-002`  
**Priority:** P0  
**Description:** Authenticate users and issue a short-lived JWT in an HttpOnly cookie plus a readable CSRF cookie according to the approved contract.

**Tasks**

- Verify passwords using the stored Argon2id hash.
- Create JWT claims for subject, issued-at, expiry, token type/version, and configured algorithm.
- Set auth cookie with HttpOnly, Secure, SameSite, path, and expiry configuration.
- Generate and set a cryptographically random CSRF cookie.
- Return safe user/session metadata without returning the JWT.
- Add signin abuse-control behavior selected in `STORY-000`.

**Acceptance criteria**

- Valid credentials establish an authenticated cookie session.
- Invalid credentials return a generic safe response.
- JWT is absent from response bodies, browser storage, logs, and rendered HTML.
- Auth and CSRF cookies have the configured security attributes.
- Repeated signin failures follow the selected rate-limit/throttling behavior.

**Dependencies:** `STORY-000`, `INFRA-002`, `DB-001`, `DB-002`.  
**Testing requirements:** Password/JWT unit tests; API cookie attribute tests; invalid/expired/tampered token tests; abuse-control tests.

### STORY-AUTH-003 — Enforce JWT, CSRF, and Origin protections

**Story ID:** `AUTH-003`  
**Priority:** P0  
**Description:** Protect all authenticated and state-changing routes with validated JWT, CSRF, and explicit Origin checks.

**Tasks**

- Add FastAPI authentication dependency to extract and validate the HttpOnly JWT cookie.
- Validate algorithm, signature, subject, token type/version, issued-at, and expiry.
- Compare CSRF cookie/header values using constant-time comparison.
- Enforce the configured Origin policy on state-changing browser requests.
- Apply protection consistently to auth logout, todo mutations, and any other state-changing route.

**Acceptance criteria**

- Missing, malformed, invalid-signature, expired, or wrong-type JWTs receive `401`.
- Missing or mismatched CSRF values receive the selected safe `403`.
- Disallowed or policy-violating Origin values receive the selected safe `403`.
- Valid same-origin state-changing requests succeed.
- Authentication identity comes only from validated token claims.

**Dependencies:** `STORY-000`, `INFRA-002`, `AUTH-002`.  
**Testing requirements:** Security regression tests for all invalid token/CSRF/Origin cases and valid browser requests.

### STORY-AUTH-004 — Implement logout and current-user session state

**Story ID:** `AUTH-004`  
**Priority:** P0  
**Description:** Provide canonical logout and current-user behavior with transparent stateless JWT semantics.

**Tasks**

- Implement `GET /api/auth/me` using the authenticated identity.
- Implement `POST /api/auth/logout` with required CSRF/Origin protection.
- Clear auth and CSRF cookies with matching scope and attributes.
- Define behavior for already-absent cookies.
- Ensure client transition to unauthenticated state.

**Acceptance criteria**

- Authenticated `/me` returns only safe current-user data.
- Logout clears both cookies and returns the documented success response.
- After logout, the client cannot use the cleared cookie session for protected requests.
- Logout does not falsely claim revocation of a copied stateless JWT; any limitation is documented.

**Dependencies:** `STORY-000`, `AUTH-003`.  
**Testing requirements:** API tests for `/me`, logout, repeated logout, cookie clearing, and post-logout protected requests.

## Epic 4: Todo Management

### STORY-TODO-001 — Implement todo creation and personal listing

**Story ID:** `TODO-001`  
**Priority:** P0  
**Description:** Allow authenticated users to create incomplete todos and list only their own todos using the approved ordering/limit contract.

**Tasks**

- Add create and list routes.
- Validate title and approved optional fields.
- Assign UUID `_id` and authenticated `user_id` server-side.
- Apply documented ordering and bounded/paginated behavior.
- Return empty list/empty-state-compatible response.

**Acceptance criteria**

- Valid input creates one incomplete todo owned by the authenticated user.
- Client-supplied `user_id`, `_id`, or protected fields cannot override server values.
- Listing returns only the current user's todos in documented order and bounds.
- Invalid or unauthenticated requests are rejected safely.

**Dependencies:** `STORY-000`, `INFRA-002`, `DB-001`, `DB-002`, `AUTH-003`.  
**Testing requirements:** API CRUD setup tests; validation tests; two-user isolation and ordering/limit tests.

### STORY-TODO-002 — Implement todo read, edit, and delete

**Story ID:** `TODO-002`  
**Priority:** P0  
**Description:** Support safe retrieval, editing of approved fields, and deletion of owned todos.

**Tasks**

- Add get, patch, and delete routes.
- Restrict update fields and preserve ownership/identifier fields.
- Return consistent safe response for missing or another user's todo.
- Update timestamps on successful edits.
- Return documented delete response.

**Acceptance criteria**

- A user can read and edit their own todo with valid input.
- Invalid edits do not change stored data.
- A user can delete their own todo and it no longer appears.
- Another user's todo cannot be read, edited, or deleted.
- `_id` and `user_id` remain unchanged through updates.

**Dependencies:** `TODO-001`, `AUTH-003`.  
**Testing requirements:** API tests for read/update/delete, invalid payloads, not-found behavior, and cross-user attempts.

### STORY-TODO-003 — Implement idempotent completion toggles

**Story ID:** `TODO-003`  
**Priority:** P0  
**Description:** Add complete and uncomplete actions with deterministic final states and ownership protection.

**Tasks**

- Add complete and uncomplete routes.
- Ensure updates are constrained by todo ID and authenticated user ID.
- Define repeated-action behavior and response shape.
- Update timestamps and return the resulting todo.

**Acceptance criteria**

- Complete changes an owned todo to `completed=true`.
- Uncomplete changes an owned todo to `completed=false`.
- Repeating either action leaves the same final state without unintended side effects.
- Another user's todo cannot be status-changed.
- Resulting task and dashboard data reflect the final state.

**Dependencies:** `TODO-002`, `DASH-001`.  
**Testing requirements:** API idempotence, ownership, timestamp, and state-transition tests.

## Epic 5: Frontend Development

### STORY-UI-001 — Build responsive authentication interface

**Story ID:** `UI-001`  
**Priority:** P0  
**Description:** Build accessible signup/signin views using HTML, Tailwind CSS, and Vanilla JavaScript against the auth API.

**Tasks**

- Implement signup and signin forms with labels and keyboard access.
- Add client-side usability validation while preserving server authority.
- Use same-origin credentials and CSRF header handling.
- Render loading, success, and safe error states.
- Transition authenticated users to the app shell.

**Acceptance criteria**

- A user can complete signup and signin through the browser.
- Invalid fields show understandable feedback without exposing secrets.
- The JWT is never accessible to JavaScript.
- Forms are usable at approved mobile and desktop viewport sizes.

**Dependencies:** `STORY-000`, `INFRA-002`, `AUTH-001`, `AUTH-002`, `AUTH-003`.  
**Testing requirements:** Browser smoke tests for signup/signin, validation, cookie behavior, accessibility labels, and responsive layouts.

### STORY-UI-002 — Build todo management interface

**Story ID:** `UI-002`  
**Priority:** P0  
**Description:** Build the authenticated todo list and controls for create, view, edit, delete, complete, and uncomplete.

**Tasks**

- Implement task form and list rendering.
- Add edit and delete interactions with safe confirmation/feedback.
- Add completion controls and state styling.
- Handle empty, loading, unauthorized, validation, and server-error states.
- Refresh/update task data after mutations.

**Acceptance criteria**

- An authenticated user can complete the full todo lifecycle through the UI.
- Only server-returned current-user tasks are displayed.
- Empty states and operation feedback are understandable.
- UI never trusts a client-provided ownership field.
- Core controls remain usable on approved mobile and desktop layouts.

**Dependencies:** `TODO-001`, `TODO-002`, `TODO-003`, `UI-001`, `DASH-001`.  
**Testing requirements:** Browser end-to-end task lifecycle; two-user isolation scenario; responsive and keyboard smoke tests.

### STORY-UI-003 — Implement authenticated navigation and logout state

**Story ID:** `UI-003`  
**Priority:** P0  
**Description:** Provide the app shell, current-user state, protected-view transitions, and logout behavior.

**Tasks**

- Implement authenticated navigation and route/view switching.
- Call `/api/auth/me` to establish safe user state.
- Handle `401` by clearing local UI state and returning to signin.
- Invoke logout with CSRF protection.
- Prevent stale protected data from remaining visible after logout.

**Acceptance criteria**

- Authenticated users can navigate dashboard and todos without re-entering credentials for a valid session.
- Logout clears authenticated UI state and protected content.
- Invalid/expired sessions return the user to an unauthenticated view safely.
- No token is stored in localStorage, sessionStorage, DOM, or application state.

**Dependencies:** `AUTH-004`, `UI-001`, `DASH-001`.  
**Testing requirements:** Browser session-expiry, logout, navigation, and stale-data tests.

## Epic 6: Dashboard

### STORY-DASH-001 — Implement user-scoped dashboard statistics

**Story ID:** `DASH-001`  
**Priority:** P0  
**Description:** Provide an authenticated dashboard endpoint and UI cards for total, completed, and incomplete todos.

**Tasks**

- Add a user-scoped aggregation pipeline for dashboard counts.
- Ensure counts are consistent within one returned response/data snapshot.
- Add dashboard route and response schema.
- Render zero-state and loading/error states.
- Refresh statistics after create, delete, complete, and uncomplete.

**Acceptance criteria**

- Dashboard returns total, completed, and incomplete counts for only the authenticated user.
- Total equals completed plus incomplete for the returned response.
- Counts update after each supported todo mutation.
- A user with no todos sees zero counts and a useful empty state.
- Cross-user todos never affect counts.

**Dependencies:** `STORY-000`, `INFRA-002`, `DB-001`, `DB-002`, `AUTH-003`, `TODO-001`.  
**Testing requirements:** Aggregation tests; two-user isolation tests; mutation-refresh API/browser tests; zero-state tests.

## Epic 7: Docker Integration

### STORY-DOCKER-001 — Containerize the application and MongoDB

**Story ID:** `DOCKER-001`  
**Priority:** P0  
**Description:** Package the FastAPI/static frontend application and MongoDB using Docker Compose with a private network and persistent database volume.

**Tasks**

- Create a pinned application image.
- Create a pinned MongoDB service with named volume.
- Configure internal service networking and application-to-MongoDB connection.
- Run application as non-root where practical.
- Keep MongoDB unexposed to the host by default.
- Add development overrides only where needed.

**Acceptance criteria**

- Documented Docker Compose startup launches app and MongoDB.
- MongoDB data persists across container recreation through the named volume.
- Application connects using external configuration, not hard-coded secrets.
- MongoDB is not publicly exposed by default.

**Dependencies:** `INFRA-001`, `DB-001`, `STORY-000`.  
**Testing requirements:** Clean Compose startup test; persistence test; service-network and configuration test.

### STORY-DOCKER-002 — Add health checks and environment configuration

**Story ID:** `DOCKER-002`  
**Priority:** P0  
**Description:** Make Docker startup reliable with MongoDB health checks, app readiness, and safe environment examples.

**Tasks**

- Add MongoDB health check.
- Add application liveness/readiness checks.
- Configure Compose dependency on MongoDB readiness.
- Provide `.env.example` with placeholders only.
- Validate production cookie/security configuration.
- Document local HTTP exception and production HTTPS requirements.

**Acceptance criteria**

- Compose reports MongoDB and application health accurately.
- Application readiness fails when MongoDB or required indexes are unavailable.
- Missing required environment values fail explicitly.
- `.env.example` contains no real credentials or signing secrets.
- Production configuration rejects insecure cookie settings.

**Dependencies:** `DB-002`, `INFRA-001`, `STORY-000`, `DOCKER-001`.  
**Testing requirements:** Health/readiness tests; missing-config tests; insecure-production-config test; clean-startup smoke test.

## Epic 8: Testing

### STORY-TEST-001 — Build authentication and security regression suite

**Story ID:** `TEST-001`  
**Priority:** P0  
**Description:** Establish repeatable tests for password security, JWT validation, cookies, CSRF, Origin, and authentication abuse controls.

**Tasks**

- Add isolated test configuration and fixtures.
- Test Argon2id hashing and wrong-password behavior.
- Test JWT claims, expiry, signature, algorithm, and token type.
- Test cookie attributes and absence of JWT in response bodies.
- Test CSRF lifecycle, constant-time comparison behavior, and Origin policy.
- Test rate-limit/throttling decision for credential endpoints.

**Acceptance criteria**

- Security tests fail for missing or invalid protections.
- Invalid credentials and token cases return safe documented responses.
- Missing/mismatched CSRF and disallowed Origin cases are rejected.
- Test fixtures never use production secrets or databases.

**Dependencies:** `AUTH-001`, `AUTH-002`, `AUTH-003`, `AUTH-004`, `DOCKER-002`.  
**Testing requirements:** Unit and API security suite; run in CI/local repeatably.

### STORY-TEST-002 — Build todo ownership and dashboard regression suite

**Story ID:** `TEST-002`  
**Priority:** P0  
**Description:** Verify every todo operation and dashboard aggregation is restricted to the authenticated user and remains consistent through mutations.

**Tasks**

- Create two-user fixtures.
- Test list, read, create, update, delete, complete, and uncomplete isolation.
- Test client ownership-field tampering.
- Test dashboard counts after each mutation and zero-state.
- Test idempotent completion actions and safe not-found behavior.

**Acceptance criteria**

- User A cannot read or mutate User B's todo through any route.
- Dashboard counts never include another user's todos.
- Ownership remains unchanged after all permitted updates.
- Repeated completion actions are deterministic.

**Dependencies:** `DB-001`, `DB-002`, `TODO-001`, `TODO-002`, `TODO-003`, `DASH-001`.  
**Testing requirements:** Repository integration and API integration suite against isolated MongoDB.

### STORY-TEST-003 — Add frontend, API contract, and release verification

**Story ID:** `TEST-003`  
**Priority:** P1  
**Description:** Verify browser journeys, API consistency, responsive behavior, Docker startup, and the complete MVP definition of done.

**Tasks**

- Add browser smoke/end-to-end scenarios for auth, task lifecycle, dashboard, and logout.
- Verify API status codes, error envelope, ordering/limits, timestamps, and health semantics.
- Run responsive checks against the approved viewport/browser matrix.
- Run formatting, linting, static/type checks, and full test suite.
- Run clean Docker Compose startup and readiness verification.

**Acceptance criteria**

- Core browser journeys pass on the approved browser/viewport matrix.
- API contract tests pass for all documented endpoints.
- Docker startup and health checks pass from a clean environment.
- Release verification covers all PRD release acceptance criteria.

**Dependencies:** `UI-002`, `UI-003`, `DOCKER-002`, `TEST-001`, `TEST-002`.  
**Testing requirements:** Full regression suite; browser automation; Compose smoke test; quality-gate report.

## Epic 9: Documentation

### STORY-DOC-001 — Document setup, API, and security behavior

**Story ID:** `DOC-001`  
**Priority:** P1  
**Description:** Provide implementation and user-facing documentation sufficient to run, evaluate, and safely configure the MVP.

**Tasks**

- Document prerequisites and Docker Compose startup.
- Document environment variables and safe secret handling.
- Document API endpoints, auth cookies, CSRF header, status codes, and error envelope.
- Document canonical login and todo fields after `STORY-000`.
- Document local versus production cookie/HTTPS behavior.
- Document task ownership and logout/stateless-token semantics.

**Acceptance criteria**

- A new developer can start the application using documented steps.
- API consumers can identify protected routes, request shapes, response shapes, and error codes.
- Documentation does not contain real secrets.
- Security limitations and production requirements are explicit.

**Dependencies:** `STORY-000`, `INFRA-002`, `AUTH-004`, `DOCKER-002`.  
**Testing requirements:** Fresh-environment documentation walkthrough; API documentation spot-check.

### STORY-DOC-002 — Publish MVP verification and operations guide

**Story ID:** `DOC-002`  
**Priority:** P1  
**Description:** Record the MVP scope, acceptance evidence, test commands, troubleshooting guidance, and production-readiness boundaries.

**Tasks**

- Document in-scope and excluded features.
- Document test commands and required isolated services.
- Document health/readiness interpretation and common startup failures.
- Document backup, HTTPS, secret rotation, monitoring, and rate-limit requirements for production.
- Record resolved Product Owner decisions and architecture assumptions.

**Acceptance criteria**

- The documented verification steps reproduce the release quality gates.
- Excluded features are clearly identified as non-MVP.
- Operators can distinguish liveness, readiness, and configuration failures.
- Production deployment limitations and required hardening are visible.

**Dependencies:** `TEST-003`, `DOCKER-002`, `DOC-001`.  
**Testing requirements:** Documentation review; execute the documented verification path from a clean checkout.

## Recommended MVP Delivery Order

1. `STORY-000` — Resolve implementation contract decisions.
2. `INFRA-001`, `INFRA-002` — Establish application and API foundations.
3. `DB-001`, `DB-002` — Establish persistence and indexes.
4. `AUTH-001` through `AUTH-004` — Complete secure authentication.
5. `TODO-001` through `TODO-003` — Complete the server-side task lifecycle.
6. `DASH-001` — Add user-scoped statistics.
7. `UI-001` through `UI-003` — Deliver the browser experience.
8. `DOCKER-001`, `DOCKER-002` — Validate repeatable container execution.
9. `TEST-001`, `TEST-002`, `TEST-003` — Run security, ownership, and release verification.
10. `DOC-001`, `DOC-002` — Publish setup and operations documentation.

This order is a recommendation for implementation sequencing; each story's explicit dependency list is authoritative.

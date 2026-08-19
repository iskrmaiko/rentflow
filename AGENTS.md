# RentFlow — Project Context for AI Agent

This file is read at the start of every conversation. It gives the AI agent full context
about RentFlow so that project memory is not lost between sessions.

---

## 1. What Is RentFlow?

RentFlow is a **fictional equipment rental management platform** built as a learning project.

It is designed to give practical, hands-on experience with a realistic business application
while progressively introducing modern technologies and architectural patterns.

**This is both a software project and a learning project.**
Do not optimize only for speed. The developer wants to understand architecture, reasoning,
trade-offs, and development workflow as we build.

---

## 2. Technology Stack

### Frontend
- SvelteKit
- TypeScript (strict mode)
- fetch API (no extra HTTP client library)

### Backend
- Python 3.12
- FastAPI
- Clean Architecture
- DDD-inspired domain modeling
- psycopg2 (synchronous PostgreSQL driver)
- Pydantic v2

### Database
- PostgreSQL 16

### Local Infrastructure
- Docker
- Docker Compose

### Future Infrastructure (do not introduce prematurely)
- Terraform (infrastructure as code)
- AWS (cloud deployment)
- Ansible + Jinja2 (configuration and provisioning)
- CI/CD

---

## 3. Current Architecture

The backend uses a **domain-oriented structure** inside a Clean Architecture boundary.

```
backend/
├── domain/
│   └── equipment/
│       ├── entities.py
│       ├── exceptions.py
│       └── repositories.py
├── application/
│   └── equipment/
│       └── use_cases.py
├── infrastructure/
│   └── equipment/
│       └── postgres_repository.py
└── api/
    ├── main.py
    └── equipment/
        ├── schemas.py
        └── router.py
```

When adding a new domain (e.g., `customer`), follow the same pattern:
`domain/customer/`, `application/customer/`, `infrastructure/customer/`, `api/customer/`.

**Dependency direction (strictly enforced):**
```
api → application → domain ← infrastructure
```
The domain layer must NEVER import FastAPI, Pydantic, psycopg2, or any framework/infrastructure library.

The frontend is also organized by feature:

```
frontend/src/
├── routes/equipment/      # SvelteKit pages
└── lib/equipment/
    ├── api.ts             # API client
    ├── types.ts           # TypeScript types
    └── components/
        └── EquipmentForm.svelte
```

Shared frontend utilities (layout, navigation) live in `routes/` root.
Equipment-specific code stays under `lib/equipment/`.
When a new domain is added, create `lib/<domain>/` following the same pattern.

---

## 4. What Has Been Completed

### Equipment Catalog (DONE ✅)
The first and currently only domain. Fully implemented and verified.

**API Endpoints:**
| Method | Path | Description | Status |
|--------|------|-------------|--------|
| GET | `/equipment` | List all equipment | ✅ |
| GET | `/equipment/{id}` | Get by ID | ✅ |
| POST | `/equipment` | Create new | ✅ |
| PUT | `/equipment/{id}` | Full update | ✅ |
| PATCH | `/equipment/{id}/toggle-status` | Soft deactivate/reactivate | ✅ |
| DELETE | `/equipment/{id}` | Permanent delete | ✅ |

**Domain Entity — Equipment:**
- `id` (UUID, system-generated)
- `name` (str, required, non-empty)
- `description` (str, may be empty)
- `category` (EquipmentCategory enum)
- `daily_rental_price` (Decimal, >= 0)
- `status` (EquipmentStatus: ACTIVE | INACTIVE)

**Key domain behavior:**
- `toggle_status()` on the entity flips ACTIVE ↔ INACTIVE (soft delete)
- `DELETE /equipment/{id}` permanently removes the DB record (hard delete)
- These two operations are intentionally SEPARATE and must not be merged

**Specs location:** `.kiro/specs/equipment-catalog/`

---

## 5. Important Architectural Principles

These must be maintained unless there is a deliberate, explained reason to change them:

- Domain layer has zero external dependencies (no FastAPI, no psycopg2, no Pydantic)
- Application layer depends only on domain abstractions (interfaces), never on infrastructure
- Infrastructure implements domain repository interfaces
- API layer handles HTTP concerns only — no business logic in routes
- Frontend does not contain backend business rules
- Avoid unnecessary coupling between domains
- Prefer explicit domain behavior (entity methods) over procedural logic scattered in routes
- Avoid premature abstraction
- Do not add technologies just to demonstrate them — introduce them when genuinely needed

---

## 6. Critical Distinction: Soft Delete vs. Hard Delete

These are intentionally different operations throughout the application:

**Soft delete (status toggle):**
- `PATCH /equipment/{id}/toggle-status`
- ACTIVE → INACTIVE or INACTIVE → ACTIVE
- Database record remains, item can be reactivated
- Pure domain method: `entity.toggle_status()`

**Hard delete (permanent):**
- `DELETE /<resource>/{id}`
- Permanently removes the database record
- Cannot be reactivated
- Returns 204 No Content on success, 404 if not found

Apply this pattern consistently to all future domains.

---

## 7. Full Domain Roadmap

**Introduce domains one at a time. Never implement the next domain without explicit approval.**

### Phase 1 — Application Architecture & Core Domains

| Domain | Status | What you learn |
|--------|--------|----------------|
| Equipment | ✅ Done | Clean Architecture, Repository pattern, Dependency Inversion, CRUD, REST |
| Customer | 🔜 Next | Domain modeling, validation, relationships |
| Reservation | Later | Business rules, domain invariants, availability, state transitions |
| Rental | Later | Richer domain behavior, relationships between aggregates, transactions |

### Phase 2 — Real Business Complexity

- Rental ↔ Reservation ↔ Equipment interactions
- Maintenance domain (equipment availability states)
- Payment / Billing domain

### Phase 3 — Production Engineering (Local → Container)

- Improved Dockerfiles
- Environment variables and configuration management
- Health checks and networking
- Development vs. production configuration
- Automated testing: unit, integration, API, frontend

### Phase 4 — Cloud Infrastructure

- Terraform: providers, variables, outputs, resources, modules, state
- AWS deployment (free-tier eligible resources preferred)
- Target: SvelteKit → AWS → FastAPI → PostgreSQL

### Phase 5 — Operations

- Ansible (configuration and provisioning)
- Jinja2 templates
- Production environment management

---

## 8. How to Add a New Domain

When introducing a new domain, always follow these steps in order.
**Do not skip steps. Do not start coding before approval.**

1. **Understand the business problem**
   - What does this domain solve?
   - Who interacts with it?
   - What business rules apply?
   - How does it relate to existing domains?

2. **Requirements** — create `.kiro/specs/<domain>/requirements.md`
   - User stories
   - Acceptance criteria
   - Domain terminology glossary
   - Important business rules

3. **Domain modeling** — create `.kiro/specs/<domain>/design.md`
   - Entities, value objects, enums
   - Domain behaviors (methods on entities)
   - Domain invariants and exceptions
   - Repository interface

4. **Architecture & Design** — extend design.md
   - Application use cases (one class per operation)
   - Infrastructure (DB schema, repository implementation)
   - API endpoints and Pydantic schemas
   - Frontend responsibilities

5. **Implementation plan** — create `.kiro/specs/<domain>/tasks.md`
   - Ordered tasks, domain → repository → use cases → API → frontend
   - Include checkpoints for verification

6. **Wait for explicit user approval before writing any code**

7. **Implement incrementally** — commit at each meaningful checkpoint

8. **Verify** — run the application, test endpoints, check frontend

9. **Review** — explain what was added, how it fits, what was learned

---

## 9. Development Workflow

### Spec-Driven Workflow
```
Requirements → Design → Implementation Plan → Approval → Tasks → Code → Verify → Review
```

### Before significant changes:
1. Inspect existing code
2. Explain the proposed change
3. Identify affected files and architectural consequences
4. Produce a plan
5. Wait for approval

### Do not:
- Modify unrelated files
- Introduce new domains without approval
- Add infrastructure technologies prematurely
- Merge soft-delete and hard-delete behavior

---

## 10. Cost Constraint

This is a learning project. Prefer:
- Free and open source tools
- Local development with Docker
- AWS free-tier eligible resources only

Before suggesting any AWS resource that could incur cost, state explicitly:
- What it costs
- Whether it has a free tier
- What could cause unexpected charges
- Whether there is a free/local alternative

---

## 11. Current Next Step

The Equipment domain is complete and verified.

**The next domain is: Customer**

Before implementing, produce:
1. `requirements.md` for Customer
2. `design.md` for Customer
3. `tasks.md` for Customer

Wait for approval before writing any code.

The Customer domain is next because:
- It reinforces domain-oriented structure patterns
- It introduces new validation patterns (email uniqueness, format)
- It is a required dependency for Reservation and Rental in Phase 1

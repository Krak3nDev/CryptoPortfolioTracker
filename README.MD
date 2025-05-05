# CryptoPortfolioTracker

*A playground project that applies Clean Architecture and **Domain‑Driven Design (DDD)** to a cryptocurrency portfolio manager.*

---

## Table of Contents
1. [Tech Stack](#tech-stack)  
2. [Getting Started](#getting-started)  
3. [Architecture](#architecture)  
4. [Reflection on Domain Choice](#reflection-on-domain-choice)  
5. [Development & Testing](#development--testing)  
   - [Backend](#backend-development--testing)  
   - [Frontend](#frontend-development--testing)  

---

## Tech Stack

### Backend
| Tool | Role |
|------|------|
| **FastAPI** | High‑performance async REST framework |
| **Dishka** | IoC container (replaces FastAPI DI) |
| **Taskiq + RabbitMQ** | Async task queue & message broker |
| **PostgreSQL** | Primary relational storage |
| **Redis** | Caching & Taskiq result backend |
| **MinIO** | S3‑compatible object storage |

### Monitoring & Observability
| Tool | Role |
|------|------|
| **VictoriaMetrics** | Time‑series DB for metrics |
| **VictoriaLogs** | Centralised log storage |
| **Grafana** | Dashboards & visualisation |
| **Vector** | Log / metric collector & shipper |

### Frontend
| Tool | Role |
|------|------|
| **Angular 19** | SPA framework |
| **NgRx (Store / Effects / Entity / Router / Component Store)** | Reactive state management |
| **RxJS** | Reactive programming primitives |
| **FontAwesome** | Icon set |
| **Jest** | Unit testing |

---

## Getting Started

### Prerequisites
* Docker + Docker Compose  
* Git

### Setup
```bash
git clone https://github.com/Krak3nDev/CryptoPortfolioTracker
cd CryptoPortfolioTracker

cp env.dist .env      # fill DB, Redis, RabbitMQ, SMTP, MinIO, CoinMarketCap keys
docker compose up -d
```

### Default End‑points
| Service | URL |
|---------|-----|
| **Backend API** (Swagger) | <http://localhost/docs> |
| **Frontend** | <http://localhost> |
| **Grafana** | <http://localhost:3000> |
| **MinIO Console** | <http://localhost:9001> |
| **RabbitMQ UI** | <http://localhost:15672> |

---

## Architecture

The project follows **DDD** with a classic 4‑layer layout:

| Layer | Eric Evans’ original description\* |
|-------|------------------------------------|
| **User Interface / Presentation** | “**Responsible for showing information to the user and interpreting the user’s commands.** The external actor might sometimes be another computer system rather than a human user.” |
| **Application** | “**Defines the jobs the software is supposed to do and directs the expressive domain objects to work out problems.** … *This layer is kept thin.* It does not contain business rules or knowledge, but only coordinates tasks and delegates work to collaborations of domain objects in the next layer down.” — In this codebase it also performs **application‑level validation** (e.g. `get_transaction_with_ownership_check`, `get_portfolio_with_ownership_check`). |
| **Domain / Model** | “**Responsible for representing concepts of the business, information about the business situation, and business rules.** State that reflects the business situation is controlled and used here, even though the technical details of storing it are delegated to the infrastructure. *This layer is the heart of business software.*” |
| **Infrastructure** | “**Provide generic technical capabilities that support the higher layers:** message sending for the application, persistence for the domain, etc.” |

\* Eric Evans, *Domain‑Driven Design: Tackling Complexity in the Heart of Software*, Chapter 4 “Layered Architecture”.

---

## Reflection on Domain Choice

> ⚠️ **Current domain = simple CRUD; full‑blown DDD brings little extra value.**

* **No real Aggregates** – entities mutate directly, complex invariants are absent.  
* **Minimal business rules** – endpoints mostly wrap Create/Read/Update/Delete.  
* **Few domain events / workflows** – little behaviour to model.  

For such a thin domain it would be perfectly fine to **treat raw SQLAlchemy models as the domain model** and operate on them directly.

Still, the project was a useful sandbox: I experimented with **SQLAlchemy imperative mapping**, Taskiq and also DDD — even if the domain itself doesn’t demand them.

---

## Development & Testing

### Backend Development & Testing
```bash
cd backend
uv sync           # install dependencies from uv.lock
pytest            # run unit & e2e tests
```

### Frontend Development & Testing
```bash
cd frontend
npm install
npm start         # http://localhost:4200 with HMR

npm test          # run Jest once
npm run test:watch
npm run test:coverage
```

---


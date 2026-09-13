# Document Processing & Signing Platform

A showcase production-oriented document processing platform built with **Python 3.12**, **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Temporal**.

## Tech Stack

| Area                   | Technology                      |
| ---------------------- | ------------------------------- |
| Language               | Python 3.12                     |
| API                    | FastAPI                         |
| Architecture           | Clean / Onion Architecture, DDD |
| Database               | PostgreSQL                      |
| ORM                    | SQLAlchemy 2.x                  |
| Migrations             | Alembic                         |
| Workflow orchestration | Temporal                        |
| XML processing         | lxml                            |
| Configuration          | Pydantic Settings               |
| Package management     | uv                              |
| Testing                | pytest / pytest-asyncio         |
| Containers             | Docker / Docker Compose         |
| Linting                | Ruff                            |

## Current Features

- Document upload and persistence
- XML schema management
- Document-to-schema association
- Document content stored separately from database metadata
- SHA-256 document content hashing
- Document processing status tracking
- XML processing and XSD validation
- Asynchronous document processing using Temporal
- Dedicated Temporal worker process
- PostgreSQL persistence using SQLAlchemy
- Database migrations with Alembic
- Clean separation between domain, application, and infrastructure layers
- REST API built with FastAPI
- Automatic Temporal activity retries

## Architecture

The backend follows a Clean / Onion Architecture approach:

```text
┌─────────────────────────────────────────────┐
│                Presentation                 │
│              FastAPI / REST API             │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│                Application                  │
│          Use Cases / Ports / UoW            │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│                  Domain                     │
│       Entities / Value Concepts / Rules     │
└─────────────────────────────────────────────┘
                       ▲
                       │
┌──────────────────────┴──────────────────────┐
│              Infrastructure                 │
│ PostgreSQL / SQLAlchemy / Files / Temporal  │
└─────────────────────────────────────────────┘
```

The dependency direction is:

```text
Infrastructure → Application → Domain
```

The application layer defines interfaces (ports), while infrastructure provides their implementations.

For example, the application layer knows that a document workflow can be started through a `DocumentWorkflowStarter` abstraction. It does not depend directly on the Temporal SDK.

## Project Structure

```text
document-platform/
├── backend/
│   ├── pyproject.toml
│   ├── .env
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── src/
│   │   └── document_platform/
│   │       ├── application/
│   │       │   ├── schemas/
│   │       │   │   └── use_cases/
│   │       │   ├── documents/
│   │       │   │   └── use_cases/
│   │       │   │
│   │       │   ├── processing/
│   │       │   │   └── ports/
│   │       │   ├── storage/
│   │       │   │   └── ports/
│   │       │   └── unit_of_work.py
│   │       │
│   │       ├── config/
│   │       │   └── settings.py
│   │       │
│   │       ├── domain/
│   │       │   ├── documents/
│   │       │   └── schemas/
│   │       │
│   │       ├── infrastructure/
│   │       │   ├── persistence/
│   │       │   ├── processing/
│   │       │   ├── storage/
│   │       │   └── temporal/
│   │       │
│   │       ├── presentation/
│   │       │   └── api/
│   │       │       └── v1/
│   │       │
│   │       └── main.py
│   │
│   └── tests/
│
├── storage/
├── docker-compose.yml
└── README.md
```

## Document Processing Flow

Document creation and processing are intentionally separated.

```text
Client
  │
  │ POST /documents
  ▼
FastAPI
  │
  ▼
CreateDocumentUseCase
  │
  ├── Validate schema
  ├── Store document
  ├── Persist metadata
  └── Commit transaction
  │
  ▼
Temporal Client
  │
  ▼
DocumentWorkflow
  │
  ▼
process_document Activity
  │
  ▼
ProcessDocumentUseCase
  │
  ├── Load document
  ├── Load XML schema
  ├── Read document content
  ├── Validate/process XML
  └── Update document status
```

The API does not wait for document processing to finish. It starts the Temporal workflow and returns after the workflow has been successfully scheduled.

Document statuses currently are:

```text
UPLOADED
    │
    ▼
PROCESSING
    │
    ├──► PROCESSED
    │
    └──► FAILED
```

## Local Development

### Prerequisites

Install:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Docker
- Docker Compose

### Start Infrastructure

From the repository root:

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- Temporal Server

The Temporal Web UI is not currently included in the Docker Compose setup.

### Backend Setup

Change into the backend directory:

```bash
cd backend
```

Install dependencies:

```bash
uv sync
```

Create the local environment configuration:

```env
POSTGRES__HOST=localhost
POSTGRES__PORT=5432
POSTGRES__USER=document_platform
POSTGRES__PASSWORD=document_platform
POSTGRES__DATABASE=document_platform_db

TEMPORAL__HOST=localhost:7233
TEMPORAL__TASK_QUEUE=document-processing
TEMPORAL__NAMESPACE=default
```

### Database Migrations

From `backend/`:

```bash
uv run alembic upgrade head
```

## Running the Application

### FastAPI

From `backend/`:

```bash
uv run uvicorn document_platform.main:app --reload
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### Temporal Worker

The Temporal worker runs as a separate process.

From `backend/`:

```bash
uv run python -m document_platform.infrastructure.temporal.worker
```

The worker polls the:

```text
document-processing
```

task queue and executes document-processing workflows and activities.

Run the API and worker in separate terminals:

```text
Terminal 1                    Terminal 2
──────────                    ──────────
FastAPI                       Temporal Worker
    │                              │
    └────────── Temporal ──────────┘
```

## Testing

From `backend/`:

```bash
uv run pytest
```

Tests are primarily focused on domain logic, application use cases, and infrastructure components.

HTTP endpoint testing is intentionally kept lightweight during development; API behavior can also be exercised through FastAPI's interactive documentation.

## Code Quality

Run Ruff:

```bash
uv run ruff check .
```

Format the code:

```bash
uv run ruff format .
```

## Database

PostgreSQL stores document and schema metadata.

Document content and XML schema files are stored separately from the relational database.

The current local storage layout is:

```text
storage/
├── documents/
│   └── <document-id>
└── schemas/
    └── <schema-id>
```

Document metadata includes:

- ID
- name
- original name
- content type
- size
- SHA-256 content hash
- schema ID
- processing status
- creation timestamp
- update timestamp

## Temporal

Temporal is used for durable asynchronous document processing.

The current workflow consists of:

```text
DocumentWorkflow
       │
       ▼
process_document
       │
       ▼
ProcessDocumentUseCase
```

Temporal provides:

- durable workflow execution
- activity retries
- workflow state persistence
- worker-based execution
- separation between API and background processing

The worker is intentionally run as a separate process to mirror a production deployment where API and background-processing workloads can be scaled independently.

## XML Processing

XML processing is implemented behind an application-level processing abstraction.

The infrastructure implementation currently uses `lxml`.

Current processing capabilities include XML parsing and optional XSD validation.

Planned XML capabilities include:

- XPath-based extraction
- Schematron validation
- richer validation results
- XML transformation where appropriate

## Roadmap

The project is being developed incrementally around the target production stack.

### Phase 1 — Core Platform

- [x] FastAPI application
- [x] Clean / Onion architecture
- [x] Domain entities
- [x] PostgreSQL persistence
- [x] SQLAlchemy
- [x] Alembic migrations
- [x] Document storage
- [x] Schema management
- [x] Document processing states
- [x] XML parsing
- [x] XSD validation

### Phase 2 — Workflow Processing

- [x] Temporal integration
- [x] Temporal client
- [x] Document workflow
- [x] Processing activity
- [x] Dedicated Temporal worker
- [x] Activity retries
- [x] Persistent processing status

### Phase 3 — Advanced XML Processing

- [ ] XPath
- [ ] Schematron
- [ ] Structured validation results
- [ ] Processing error model

### Phase 4 — Digital Signatures

- [ ] PKI concepts and certificate handling
- [ ] X.509 certificates
- [ ] CSR generation
- [ ] XML signatures
- [ ] XAdES
- [ ] Signature validation

### Phase 5 — Production Infrastructure

- [ ] Dockerized application and worker
- [ ] AWS deployment
- [ ] CI/CD with GitHub Actions
- [ ] Configuration management
- [ ] Observability
- [ ] Structured logging
- [ ] Health checks
- [ ] Production database configuration

### Phase 6 — Frontend

- [ ] React + TypeScript operator console
- [ ] Document management
- [ ] Schema management
- [ ] Processing status
- [ ] Validation results
- [ ] Workflow monitoring

## Development Philosophy

The project intentionally favors explicit architecture over framework-specific magic.

Key principles:

- Domain logic does not depend on infrastructure.
- Application use cases depend on abstractions rather than concrete infrastructure implementations.
- Infrastructure concerns remain outside the domain.
- Long-running processing is handled by Temporal rather than API background tasks.
- Database transactions are explicit.
- Document content is separated from document metadata.
- Processing is designed to be retryable and independently scalable.

The project is developed incrementally, with each feature implemented as a realistic production-oriented capability rather than as an isolated technology demonstration.

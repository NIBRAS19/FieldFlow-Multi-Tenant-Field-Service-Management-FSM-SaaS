# FieldFlow — Multi-Tenant Field Service Management (FSM) SaaS

[![Django](https://img.shields.io/badge/Django-5.2+-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16+-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15.0+-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

> **FieldFlow** is an enterprise-grade, multi-tenant Field Service Management (FSM) platform architected for modern commercial and residential service businesses (HVAC, electrical, plumbing, facilities maintenance, and specialized equipment servicing). It streamlines the entire operational lifecycle from customer intake and dispatch scheduling to mobile execution, proof-of-work capture, customer e-signatures, and automated billing.

---

## Table of Contents

1. [Executive Summary & Project Overview](#1-executive-summary--project-overview)
2. [Key Capabilities & Feature Matrix](#2-key-capabilities--feature-matrix)
3. [Technology Stack](#3-technology-stack)
4. [System Architecture & Design](#4-system-architecture--design)
5. [Repository & Directory Structure](#5-repository--directory-structure)
6. [Prerequisites & Installation](#6-prerequisites--installation)
7. [Environment Variables & Configuration](#7-environment-variables--configuration)
8. [Application Workflows & User Journeys](#8-application-workflows--user-journeys)
9. [User Roles & Permissions Matrix](#9-user-roles--permissions-matrix)
10. [REST API Documentation & Endpoints](#10-rest-api-documentation--endpoints)
11. [Database Schema & Entity-Relationship Model](#11-database-schema--entity-relationship-model)
12. [Core Business Logic & State Machines](#12-core-business-logic--state-machines)
13. [Development Commands & Tooling](#13-development-commands--tooling)
14. [Testing & Quality Assurance](#14-testing--quality-assurance)
15. [Security & Compliance Controls](#15-security--compliance-controls)
16. [Integrations & External Services](#16-integrations--external-services)
17. [Docker & Production Deployment](#17-docker--production-deployment)
18. [Troubleshooting & Frequently Asked Questions](#18-troubleshooting--frequently-asked-questions)
19. [Roadmap & Future Enhancements](#19-roadmap--future-enhancements)
20. [Contributing & Code Standards](#20-contributing--code-standards)
21. [License, Credits & Maintainers](#21-license-credits--maintainers)

---

## 1. Executive Summary & Project Overview

### 1.1 The Problem
Field service operations frequently suffer from fragmented communication, disconnected software tools, and delayed billing cycles. Service businesses typically encounter:
- **Disjointed Communication:** Customer service requests arrive via disparate channels (phone, email, WhatsApp) without centralized tracking or SLA accountability.
- **Dispatch Inefficiencies:** Dispatchers lack visibility into technician availability, job locations, route statuses, and skill proficiencies.
- **Lost Proof-of-Work:** Field technicians rely on paper work orders, risking lost job checklists, unbilled parts, missing photo documentation, and unsigned service approvals.
- **Delayed Invoicing:** Delays between job sign-off and back-office invoicing lead to prolonged billing cycles and impaired cash flow.

### 1.2 The Solution
**FieldFlow** resolves operational friction by unifying the entire field service lifecycle into a multi-tenant cloud platform:
1. **Multi-Tenant SaaS Foundation:** Secure data isolation by organization with custom operating hours, regional currency (e.g., AED, USD), and timezone management.
2. **End-to-End Service Pipeline:** Clean state progression from `Service Request` &rarr; `Work Order` &rarr; `Technician Dispatch` &rarr; `Field Checklist & Parts Consumption` &rarr; `Customer E-Signature` &rarr; `Itemized Invoicing & Payment`.
3. **Tri-Perspective Interfaces:**
   - **Operations Command Center:** Web console for dispatchers and managers to monitor live KPIs, manage calendars, and assign jobs.
   - **Technician Mobile Experience:** Streamlined mobile view for field crews to update travel statuses, execute step-by-step checklists, log used materials, upload media, and capture client signatures.
   - **Customer Self-Service Portal:** Client portal to submit new service requests, monitor scheduled visits, review service history, and inspect outstanding balances.

### 1.3 Implementation Status
- **Backend (`fieldflow-backend`):** Fully implemented, production-architected Django 5.2 / DRF REST API with JWT authentication, tenant isolation middleware/services, PostgreSQL support with automatic SQLite fallback, comprehensive models, audit logging, and automated demo seeding (`seed_demo`).
- **Frontend (`fieldflow-frontend`):** Next.js App Router (React 19, TypeScript, Tailwind CSS v4) with responsive operational views, interactive schedule board, dispatch kanban, customer portal, and technician mobile views. Currently renders mock operational datasets and client state, designed for direct integration with the Django REST API.

---

## 2. Key Capabilities & Feature Matrix

| Functional Domain | Implemented Features | Business Impact |
| :--- | :--- | :--- |
| **Multi-Tenancy & RBAC** | Organization isolation via header/query context; user membership roles (`owner`, `admin`, `operations`, `dispatcher`, `technician`, `finance`, `customer`). | Ensures complete data isolation for SaaS tenants while maintaining granular role permissions. |
| **Customer & Asset CRM** | Customer directories, multi-location support with geospatial coordinates (`latitude`/`longitude`), asset registries with serial numbers, warranty expiry, and maintenance due tracking. | Provides historical asset maintenance context, reducing first-time fix failures. |
| **Service Request Intake** | Numbered ticket creation (`REQ-XXXX`), priority classification (`low`, `medium`, `high`, `urgent`), preferred time slots, and single-click work order conversion. | Eliminates dropped requests and enforces SLA triage from the moment an issue is reported. |
| **Work Order Management** | Sequential work orders (`WO-XXXX`), SLA due dates, estimated vs. actual duration metrics, and enforced state machine transitions. | Standardizes field execution standards and tracks operational metrics across all jobs. |
| **Dispatch & Scheduling** | Dispatch board with real-time technician workload, unassigned queue, status indicators (`Available`, `En Route`, `On Site`, `Offline`), and hourly schedule board. | Maximizes technician utilization and reduces transit and idle time. |
| **Field Execution & Proof-of-Work** | Interactive checklist templates, ad-hoc checklist items, real-time inventory deduction for parts/materials, media attachments (`photo`, `document`), and digital canvas customer e-signatures. | Prevents warranty disputes, guarantees quality standards, and captures legally binding sign-offs. |
| **Billing & Invoicing** | Automated invoice generation (`INV-XXXXXXXX`), line item management, inventory pricing linkage, payment status tracking (`Draft`, `Sent`, `Partial`, `Paid`, `Overdue`), and revenue reporting. | Reduces days sales outstanding (DSO) by converting completed jobs directly into itemized invoices. |
| **Audit Trails & Security** | Immutable audit logs capturing actor, action, resource, timestamp, IP address, user agent, and before/after JSON diffs. | Delivers enterprise compliance, transparency, and operational forensics. |
| **Portals & Mobile Interfaces** | Dedicated `/portal` for end-customers to track service visits; dedicated `/technician` mobile console for on-site execution. | Enhances customer satisfaction while empowering field crews with a frictionless UI. |

---

## 3. Technology Stack

### 3.1 Backend Architecture
- **Framework:** Python 3.12, [Django 5.2+](https://www.djangoproject.com/)
- **API Engine:** [Django REST Framework (DRF) 3.16+](https://www.django-rest-framework.org/)
- **Authentication:** [djangorestframework-simplejwt 5.5+](https://github.com/jazzband/djangorestframework-simplejwt) (JWT Access & Refresh tokens with token rotation)
- **Database Engine:** [PostgreSQL 17](https://www.postgresql.org/) via [`psycopg[binary] 3.2+`](https://www.psycopg.org/) (Production/Docker); automatic fallback to **SQLite 3** for rapid zero-dependency local development
- **CORS Handling:** [`django-cors-headers 4.7+`](https://github.com/adamchainz/django-cors-headers)
- **Image & File Handling:** [`Pillow 11.3+`](https://python-pillow.org/)
- **Configuration & Environment:** [`python-dotenv 1.1+`](https://github.com/theskumar/python-dotenv)

### 3.2 Frontend Architecture
- **Framework:** [Next.js 15+ (App Router)](https://nextjs.org/)
- **Core Library:** [React 19](https://react.dev/)
- **Type System:** [TypeScript 5+](https://www.typescriptlang.org/)
- **Styling:** [Tailwind CSS v4](https://tailwindcss.com/) via `@tailwindcss/postcss` and tailored CSS custom properties
- **Iconography:** [Lucide React](https://lucide.dev/)
- **Fonts & Typography:** Inter / System UI sans-serif

### 3.3 Infrastructure & Tooling
- **Containerization:** Docker (`python:3.12-slim`), Docker Compose (orchestrating `api` and `db` services)
- **Database Service:** PostgreSQL 17 Alpine Docker image with persistent volumes
- **Code Quality:** ESLint (`eslint-config-next`), Django check & test runner

---

## 4. System Architecture & Design

### 4.1 High-Level Architecture Diagram

```mermaid
flowchart TB
    subgraph ClientLayer["Frontend Client Layer (Next.js 15 / React 19)"]
        UI_Dash["Operations Console\n(/app/dashboard, /app/dispatch)"]
        UI_Tech["Technician Mobile View\n(/technician)"]
        UI_Cust["Customer Portal\n(/portal)"]
    end

    subgraph APIGateway["API Gateway & Security Layer"]
        CORS["CORS Middleware"]
        JWT["SimpleJWT Authentication"]
        OrgResolver["Tenant Context Resolver\n(X-Organization-ID Header)"]
        RBAC["Role-Based Access Control\n(Membership Validator)"]
    end

    subgraph ServiceLayer["Business Logic & Service Layer (Django REST Framework)"]
        Accounts["Accounts & Auth App"]
        Organizations["Organizations & Memberships App"]
        Customers["Customers, Locations & Assets App"]
        Operations["Operations & Dispatch App\n(Work Orders, Checklists, Materials)"]
        Invoices["Billing & Invoices App\n(Items, Recalculation, Payments)"]
        Audit["Audit & Notification App\n(Action Logs, JSON Snapshots)"]
    end

    subgraph DataStorage["Persistence & Storage Layer"]
        DB[("PostgreSQL 17 / SQLite 3\nRelational Database")]
        Media["Media Storage\n(Work Order Photos & Signatures)"]
    end

    ClientLayer -->|REST / JSON| CORS
    CORS --> JWT
    JWT --> OrgResolver
    OrgResolver --> RBAC

    RBAC --> Accounts
    RBAC --> Organizations
    RBAC --> Customers
    RBAC --> Operations
    RBAC --> Invoices
    RBAC --> Audit

    Accounts --> DB
    Organizations --> DB
    Customers --> DB
    Operations --> DB
    Operations --> Media
    Invoices --> DB
    Audit --> DB
```

### 4.2 Multi-Tenant Data Isolation Strategy
FieldFlow enforces strict tenant boundaries at the database and application levels:
1. **Model Tenancy:** Every core entity (`Customer`, `ServiceLocation`, `Asset`, `ServiceType`, `Technician`, `ServiceRequest`, `WorkOrder`, `Material`, `Invoice`, `AuditLog`, `Notification`) has a direct foreign key relationship with the `Organization` model.
2. **Context Resolution (`get_current_org`):**
   - Incoming requests are evaluated for an `X-Organization-ID` header (or fallback query/body parameter).
   - The user's active memberships (`Membership` model) are verified against the specified organization.
   - If no header is provided, the user's primary active organization is automatically loaded.
   - Cross-tenant requests or unauthorized organization IDs result in an immediate `400 Validation Error` or `403 Forbidden`.
3. **Queryset Scoping:** Every ViewSet inherits from an organization mixin (`OrgMixin` / `OrgViewSetMixin`) ensuring all querysets filter strictly by `organization=self.get_org()`.

---

## 5. Repository & Directory Structure

```text
fieldflow/
├── fieldflow-backend/             # Django REST Framework Backend
│   ├── apps/                      # Django Applications
│   │   ├── accounts/              # User models, authentication views, serializers
│   │   │   ├── models.py          # Custom User model with Role choices
│   │   │   ├── serializers.py     # Login, Register, User serializers
│   │   │   └── views.py           # RegisterView, LoginView, MeView
│   │   ├── audit/                 # System audit trails and event logging
│   │   │   ├── models.py          # AuditLog with before/after JSON diffs
│   │   │   ├── serializers.py     # AuditLogSerializer
│   │   │   └── views.py           # Read-only AuditLogViewSet
│   │   ├── customers/             # Customer CRM, locations, and asset tracking
│   │   │   ├── models.py          # Customer, ServiceLocation, Asset models
│   │   │   ├── serializers.py     # Customer, Location, Asset serializers
│   │   │   └── views.py           # Customer, Location, Asset ViewSets
│   │   ├── invoices/              # Billing, invoice items, and payment reconciliation
│   │   │   ├── models.py          # Invoice, InvoiceItem, Payment models
│   │   │   ├── serializers.py     # Invoice, Item, Payment serializers
│   │   │   ├── services.py        # Invoice numbering (INV-XXXX) and recalculation
│   │   │   └── views.py           # InvoiceViewSet with payment actions
│   │   ├── operations/            # Core field operations, dispatch, and work orders
│   │   │   ├── management/        # Custom management commands
│   │   │   │   └── commands/      # seed_demo.py command for instant demo data
│   │   │   ├── models.py          # WorkOrder, ServiceRequest, Technician, Materials, etc.
│   │   │   ├── serializers.py     # WorkOrder, Checklist, Material, Signature serializers
│   │   │   ├── services.py        # Sequence generator, audit recorder, assignment logic
│   │   │   └── views.py           # WorkOrder, Request, Dispatch, Dashboard ViewSets
│   │   └── organizations/         # Multi-tenant organization and membership models
│   │       ├── models.py          # Organization and Membership models
│   │       ├── serializers.py     # Organization and Membership serializers
│   │       ├── services.py        # get_current_org and is_manager security helpers
│   │       └── views.py           # Organization and Membership ViewSets
│   ├── config/                    # Django project configuration
│   │   ├── asgi.py                # ASGI entrypoint
│   │   ├── settings.py            # Project settings, JWT config, Database resolution
│   │   ├── urls.py                # Root URL dispatcher and router registrations
│   │   └── wsgi.py                # WSGI entrypoint
│   ├── .env                       # Local environment variables (git-ignored)
│   ├── .env.example               # Template environment configuration
│   ├── .gitignore                 # Backend gitignore rules
│   ├── db.sqlite3                 # Local SQLite development database
│   ├── Dockerfile                 # Container build instructions (Python 3.12-slim)
│   ├── docker-compose.yml         # Container orchestration (API + PostgreSQL 17)
│   ├── manage.py                  # Django management script
│   ├── README.md                  # Backend technical documentation
│   └── requirements.txt           # Python package dependencies
│
├── fieldflow-frontend/            # Next.js App Router Frontend
│   ├── app/                       # Next.js App Router routes
│   │   ├── app/                   # Operations console routes
│   │   │   └── [[...slug]]/       # Dynamic catch-all router for /app/*
│   │   │       └── page.tsx       # Renders AppRouter with requested page
│   │   ├── portal/                # Customer self-service portal
│   │   │   └── page.tsx           # Customer ticket status and billing view
│   │   ├── technician/            # Technician mobile execution interface
│   │   │   └── page.tsx           # Step-by-step checklist, notes, and completion
│   │   ├── globals.css            # Design tokens, variables, and responsive layout
│   │   ├── layout.tsx             # Root HTML layout with viewport & font metadata
│   │   └── page.tsx               # Product landing page with live KPI preview
│   ├── components/                # React UI components
│   │   └── fieldflow.tsx          # Full operations workspace (Dashboard, Dispatch, etc.)
│   ├── lib/                       # Utilities and domain models
│   │   └── data.ts                # Navigation menus and representative domain datasets
│   ├── .gitignore                 # Frontend gitignore rules
│   ├── next-env.d.ts              # Next.js TypeScript declarations
│   ├── package.json               # Node dependencies and project scripts
│   ├── package-lock.json          # Deterministic dependency lockfile
│   ├── postcss.config.mjs         # PostCSS configuration for Tailwind CSS v4
│   ├── README.md                  # Frontend technical overview
│   └── tsconfig.json              # TypeScript compiler configuration
│
└── README.md                      # Comprehensive project documentation
```

---

## 6. Prerequisites & Installation

### 6.1 Prerequisites
Ensure the following runtimes and tools are installed on your workstation:
- **Python:** Version 3.12 or higher ([Download Python](https://www.python.org/downloads/))
- **Node.js:** Version 18.x, 20.x, or 22.x LTS ([Download Node.js](https://nodejs.org/))
- **Package Manager:** `npm` (bundled with Node.js)
- **Docker & Docker Compose (Optional):** Required for containerized execution with PostgreSQL ([Docker Desktop](https://www.docker.com/products/docker-desktop/))
- **Git:** For version control ([Download Git](https://git-scm.com/))

---

### 6.2 Option A: Local Development Setup (Quickest)

#### Step 1: Set Up Backend (`fieldflow-backend`)

1. Open your terminal and navigate to the backend directory:
   ```bash
   cd fieldflow-backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell / Command Prompt)
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create your local environment file:
   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```
   *(Note: By default, leaving `DATABASE_URL` commented out or empty instructs Django to use SQLite `db.sqlite3` automatically, requiring zero local database installation).*

5. Apply database schema migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Seed the database with comprehensive demo data:
   ```bash
   python manage.py seed_demo
   ```
   *This command provisions the `FieldFlow Demo` organization, creates customer accounts (ABC Trading, Nexa Facilities, etc.), service locations, technicians, service types, service requests, work orders, and inventory materials.*

7. Start the Django development server:
   ```bash
   python manage.py runserver 8000
   ```
   *The API will be operational at `http://127.0.0.1:8000/api/v1/`.*

---

#### Step 2: Set Up Frontend (`fieldflow-frontend`)

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd fieldflow-frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   *The web client will be accessible at `http://localhost:3000`.*

---

### 6.3 Option B: Containerized Setup (Docker Compose)

The repository provides a complete multi-container setup with PostgreSQL 17 and the Django backend:

1. Navigate to the backend directory:
   ```bash
   cd fieldflow-backend
   ```

2. Launch the PostgreSQL database and backend API containers:
   ```bash
   docker compose up --build -d
   ```

3. Populate the PostgreSQL container with initial demo data:
   ```bash
   docker compose exec api python manage.py seed_demo
   ```

4. Verify container health:
   ```bash
   docker compose ps
   ```

---

### 6.4 Verifying the Installation

Open your browser and verify the operational endpoints:

| Application Layer | URL | Description | Default Credentials |
| :--- | :--- | :--- | :--- |
| **Landing Page** | `http://localhost:3000/` | Product landing page & overview | Public |
| **Operations Console** | `http://localhost:3000/app/dashboard` | Main dispatch & work order workspace | Public Prototype View |
| **Customer Portal** | `http://localhost:3000/portal` | Client self-service portal | Public Prototype View |
| **Technician Mobile** | `http://localhost:3000/technician` | Technician mobile workflow interface | Public Prototype View |
| **Backend REST API** | `http://127.0.0.1:8000/api/v1/` | DRF Browsable API Root | Requires JWT / Bearer Token |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | Superuser administration portal | `nibras` / `FieldFlow123!` |

---

## 7. Environment Variables & Configuration

The backend reads configuration settings using `python-dotenv` from `fieldflow-backend/.env`.

| Variable | Type | Default Value | Purpose & Security Context | Required? |
| :--- | :--- | :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | String | `unsafe-dev-secret-key` | Cryptographic signing key for sessions, CSRF, and tokens. Must be randomized in production. | **Yes** (in production) |
| `DJANGO_DEBUG` | Boolean | `true` | Enables detailed debug pages and browsable API. Must be `false` in production. | Optional |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated | `127.0.0.1,localhost` | Whitelisted host/domain headers to prevent HTTP Host header attacks. | **Yes** (in production) |
| `DATABASE_URL` | URI String | *(Empty string)* | Connection URI for PostgreSQL (`postgresql://user:pass@host:5432/dbname`). If omitted, falls back to SQLite `db.sqlite3`. | Optional |
| `CORS_ALLOWED_ORIGINS` | Comma-separated | `http://localhost:3000` | Whitelisted origins permitted to make cross-origin HTTP requests. | **Yes** |
| `DEFAULT_FROM_EMAIL` | Email String | `no-reply@fieldflow.local` | Default sender address for system notifications and alerts. | Optional |

> [!WARNING]
> Never commit active production secret keys or production database credentials to version control. Set `DJANGO_DEBUG=false` whenever deploying to public networks.

---

## 8. Application Workflows & User Journeys

### 8.1 Journey 1: Customer Service Intake to Work Order Conversion
```text
Customer submits issue via portal or phone call
                │
                ▼
Dispatcher logs Service Request (status: NEW, priority: HIGH)
                │
                ▼
Dispatcher evaluates issue, location, and required skills (status: IN_REVIEW)
                │
                ▼
Dispatcher clicks "Convert to Work Order" (POST /api/v1/requests/{id}/convert/)
                │
                ▼
Work Order WO-XXXX created (status: UNASSIGNED); Service Request marked CONVERTED
```

### 8.2 Journey 2: Dispatch, Scheduling, and Assignment
1. **Queue Inspection:** Dispatcher opens the Dispatch Board (`/app/dispatch`), reviewing unassigned work orders against technician availability cards.
2. **Technician Allocation:** Dispatcher assigns primary technician Ahmed Hassan and sets the scheduled service window (`10:00–12:00`).
3. **Status Progression:** The work order shifts to `ASSIGNED` or `SCHEDULED`, and an internal notification is generated for the technician.

### 8.3 Journey 3: Field Execution, Proof-of-Work, and Sign-off
1. **Departure (`EN_ROUTE`):** Technician marks departure on the mobile interface.
2. **Arrival (`ON_SITE`):** Upon arrival at the client site, the technician sets status to `ON_SITE`. The system automatically records the `actual_arrival` timestamp.
3. **Execution (`IN_PROGRESS`):**
   - Technician commences diagnostic procedures; `actual_start` timestamp is recorded.
   - Technician completes mandated checklist steps (`Check filter`, `Check refrigerant`, `Inspect condenser`).
   - Technician logs consumed inventory materials (e.g., 1x `AC Filter` at AED 75.00), automatically decrementing central warehouse stock.
   - Technician captures and uploads photographic evidence (`kind: photo`).
4. **Customer Approval:** Customer inspects completed work, types name, and signs directly on the touch screen canvas (`CustomerSignature`).
5. **Completion (`COMPLETED`):** Technician marks job completed; `actual_completed` timestamp is recorded. The system enforces customer signature presence before permitting technician-driven completion.

### 8.4 Journey 4: Invoicing and Payment Reconciliation
1. **Invoice Generation:** Finance team or automated trigger converts completed work order into `INV-XXXXXXXX`.
2. **Line Item Consolidation:** Labor charges and consumed materials are itemized, calculating subtotal, tax, and final balance.
3. **Payment Collection:** Customer pays via bank transfer or credit card; payment is logged against the invoice (`POST /api/v1/invoices/{id}/payments/`).
4. **Reconciliation:** When accumulated payments meet or exceed the total, the invoice status transitions to `PAID`.

---

## 9. User Roles & Permissions Matrix

FieldFlow utilizes a Role-Based Access Control (RBAC) model implemented in `apps.accounts.models.User.Role` and enforced via `apps.organizations.services.is_manager`.

| Role | Role Identifier | Primary Responsibilities |
| :--- | :--- | :--- |
| **Owner** | `owner` | Organization creator with complete administrative, billing, operational, and destructive permissions. |
| **Admin** | `admin` | System administrator managing user memberships, organization settings, and operational configurations. |
| **Operations Manager**| `operations` | Oversees daily operational flow, SLA compliance, technician scheduling, and unassigned queues. |
| **Dispatcher** | `dispatcher` | Triages incoming service requests, schedules work orders, and assigns technicians based on availability. |
| **Technician** | `technician` | Field crew executing assigned work orders, filling checklists, logging materials, and capturing signatures. |
| **Finance** | `finance` | Manages customer billing, invoice generation, payment reconciliation, and revenue reporting. |
| **Customer** | `customer` | Client representative viewing service history, tracking open visits, and submitting service requests. |

### 9.1 Permissions Matrix

| Feature / Action | Owner | Admin | Operations | Dispatcher | Technician | Finance | Customer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Manage Organization Settings** | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :x: | :x: |
| **Invite / Manage Memberships** | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :x: | :x: |
| **Create / Edit Customers & Locations** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Read-Only | Read-Only | :x: |
| **Triage & Convert Service Requests** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | Submit Only |
| **Assign / Schedule Work Orders** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: |
| **Execute Assigned Jobs & Checklists**| :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: |
| **Override Completion w/o Signature** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: |
| **Manage Invoices & Record Payments** | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :white_check_mark: | :x: |
| **View Organization Audit Logs** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :x: |

---

## 10. REST API Documentation & Endpoints

Base URL: `http://localhost:8000/api/v1/`

### 10.1 Authentication & Profile Endpoints
All protected endpoints require an `Authorization: Bearer <access_token>` header.

#### Register New Organization & Owner
- **Endpoint:** `POST /api/v1/auth/register/`
- **Access:** Public
- **Request Payload:**
  ```json
  {
    "username": "salman_owner",
    "first_name": "Salman",
    "last_name": "Al Ameri",
    "email": "salman@alameriservices.ae",
    "password": "SecurePassword123!",
    "phone": "+971501112233",
    "organization_name": "Al Ameri Facility Services LLC"
  }
  ```
- **Response (`201 Created`):**
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 12,
      "username": "salman_owner",
      "first_name": "Salman",
      "last_name": "Al Ameri",
      "email": "salman@alameriservices.ae",
      "phone": "+971501112233",
      "role": "owner",
      "timezone": "Asia/Dubai",
      "avatar": null,
      "is_active": true
    },
    "organization": {
      "id": 4,
      "name": "Al Ameri Facility Services LLC"
    }
  }
  ```

#### Authenticate (Login)
- **Endpoint:** `POST /api/v1/auth/login/`
- **Access:** Public
- **Request Payload:**
  ```json
  {
    "username": "nibras",
    "password": "FieldFlow123!"
  }
  ```
- **Response (`200 OK`):** Returns `access`, `refresh`, and user profile data.

#### Token Refresh
- **Endpoint:** `POST /api/v1/auth/refresh/`
- **Request Payload:** `{ "refresh": "<refresh_token>" }`
- **Response (`200 OK`):** Returns new `access` token.

#### Get Current User Profile
- **Endpoint:** `GET /api/v1/auth/me/`
- **Access:** Authenticated

---

### 10.2 Operations & Work Order Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/dashboard/` | Real-time counts (jobs today, unassigned, in progress, revenue, overdue). |
| `GET` | `/api/v1/dispatch/` | Technician workloads and unassigned work orders queue. |
| `GET` | `/api/v1/technician/today/` | Returns jobs assigned to the authenticated technician for today. |
| `GET` / `POST` | `/api/v1/requests/` | List or submit new customer service requests. |
| `POST` | `/api/v1/requests/{id}/convert/` | Converts an approved service request into an active work order. |
| `GET` / `POST` | `/api/v1/work-orders/` | List and create work orders (supports `?status=`, `?technician=`, `?date=`). |
| `POST` | `/api/v1/work-orders/{id}/assign/` | Assigns or reassigns technician (`{ "technician_id": 2 }`). |
| `POST` | `/api/v1/work-orders/{id}/transition/` | Advances state (`{ "status": "on_site" }`). Requires signature for completion. |
| `POST` | `/api/v1/work-orders/{id}/checklist/` | Appends checklist item (`{ "label": "Pressure test", "required": true }`). |
| `PATCH` | `/api/v1/work-orders/{id}/checklist/{item_id}/` | Updates item status (`{ "status": "completed", "note": "Normal range" }`). |
| `POST` | `/api/v1/work-orders/{id}/materials/` | Deducts parts from inventory and adds to work order itemization. |
| `POST` | `/api/v1/work-orders/{id}/signature/` | Saves customer e-signature (`customer_name`, `signature_data`). |
| `POST` | `/api/v1/work-orders/{id}/attachment/` | Uploads multipart file or on-site photo (`file`, `kind`, `caption`). |

#### Example cURL: Assign Technician to Work Order
```bash
curl -X POST http://localhost:8000/api/v1/work-orders/1/assign/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "X-Organization-ID: 1" \
  -H "Content-Type: application/json" \
  -d '{"technician_id": 2}'
```

---

### 10.3 CRM & Invoicing Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` / `POST` | `/api/v1/customers/` | List / create customer accounts. |
| `GET` / `POST` | `/api/v1/locations/` | Manage service locations with coordinates and access codes. |
| `GET` / `POST` | `/api/v1/assets/` | Track machinery and equipment warranty and service schedules. |
| `GET` / `POST` | `/api/v1/materials/` | Manage parts catalog, unit costs, and inventory stock quantities. |
| `GET` / `POST` | `/api/v1/invoices/` | List and generate customer invoices. |
| `POST` | `/api/v1/invoices/{id}/items/` | Add billable line items and trigger total recalculation. |
| `POST` | `/api/v1/invoices/{id}/payments/` | Record partial or full payment (`amount`, `method`, `reference`). |
| `POST` | `/api/v1/invoices/{id}/mark_paid/` | Automatically settles remaining balance and marks invoice as `PAID`. |
| `GET` | `/api/v1/audit-logs/` | Query organizational audit trail with before/after state diffs. |

---

## 11. Database Schema & Entity-Relationship Model

```mermaid
erDiagram
    ORGANIZATION ||--o{ USER : owns
    ORGANIZATION ||--o{ MEMBERSHIP : has
    USER ||--o{ MEMBERSHIP : joins
    ORGANIZATION ||--o{ CUSTOMER : owns
    CUSTOMER ||--o{ SERVICELOCATION : has
    CUSTOMER ||--o{ ASSET : owns
    SERVICELOCATION ||--o{ ASSET : houses

    ORGANIZATION ||--o{ TECHNICIAN : employs
    USER ||--|| TECHNICIAN : profiles

    ORGANIZATION ||--o{ SERVICETYPE : defines
    ORGANIZATION ||--o{ SERVICEREQUEST : receives
    CUSTOMER ||--o{ SERVICEREQUEST : requests
    SERVICEREQUEST ||--o| WORKORDER : converts_to

    ORGANIZATION ||--o{ WORKORDER : manages
    CUSTOMER ||--o{ WORKORDER : billed_to
    SERVICELOCATION ||--o{ WORKORDER : executed_at
    ASSET ||--o{ WORKORDER : maintains

    WORKORDER ||--o{ WORKORDERASSIGNMENT : assigned_to
    TECHNICIAN ||--o{ WORKORDERASSIGNMENT : receives

    WORKORDER ||--o{ WORKORDERCHECKLISTITEM : requires
    WORKORDER ||--o{ WORKORDERMATERIAL : consumes
    ORGANIZATION ||--o{ MATERIAL : stocks
    MATERIAL ||--o{ WORKORDERMATERIAL : fulfills

    WORKORDER ||--o{ ATTACHMENT : contains
    WORKORDER ||--o| CUSTOMERSIGNATURE : signed_by

    ORGANIZATION ||--o{ INVOICE : bills
    CUSTOMER ||--o{ INVOICE : pays
    WORKORDER ||--o{ INVOICE : originates_from
    INVOICE ||--o{ INVOICEITEM : details
    INVOICE ||--o{ PAYMENT : settles

    ORGANIZATION ||--o{ AUDITLOG : records
    ORGANIZATION ||--o{ NOTIFICATION : alerts
```

### 11.1 Key Database Entities & Constraints

1. **`Organization`**
   - Unique slug constraint (`unique=True`).
   - Regional fields: `currency` (default `AED`), `timezone` (`Asia/Dubai`), `workday_start` (`08:00`), `workday_end` (`18:00`).
2. **`Membership`**
   - Composite uniqueness constraint: `UniqueConstraint(fields=['organization', 'user'], name='uniq_org_user')`.
3. **`ServiceRequest` & `WorkOrder`**
   - Human-readable scoped sequence numbers: `request_no` (`REQ-XXXX`), `work_order_no` (`WO-XXXX`).
   - Composite uniqueness per organization: `UniqueConstraint(fields=['organization', 'work_order_no'], name='uniq_work_order_org')`.
4. **`Material` & `WorkOrderMaterial`**
   - Scoped SKU uniqueness: `UniqueConstraint(fields=['organization', 'sku'], name='uniq_material_org')`.
   - Automatic decimal inventory adjustments upon work order allocation.
5. **`CustomerSignature`**
   - Strict one-to-one mapping (`OneToOneField(WorkOrder, related_name='signature')`).
   - Stores raw vector signature data, signer name, submission timestamp, and client IP address for non-repudiation.
6. **`AuditLog`**
   - Structured JSON diff fields: `before: JSONField`, `after: JSONField`, plus `actor_id`, `action`, `resource`, `resource_id`, `ip_address`, and `user_agent`.

---

## 12. Core Business Logic & State Machines

### 12.1 Work Order State Machine

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> UNASSIGNED : Submit for Dispatch
    UNASSIGNED --> ASSIGNED : Assign Technician
    UNASSIGNED --> SCHEDULED : Schedule Time Window
    ASSIGNED --> SCHEDULED : Set Scheduled Window
    SCHEDULED --> EN_ROUTE : Technician Departs
    EN_ROUTE --> ON_SITE : Technician Arrives (actual_arrival)
    ON_SITE --> IN_PROGRESS : Technician Starts Work (actual_start)
    IN_PROGRESS --> WAITING : Pending Parts / Access
    WAITING --> IN_PROGRESS : Resume Work
    IN_PROGRESS --> COMPLETED : Customer Signs & Submit
    ON_SITE --> COMPLETED : Manager Override
    COMPLETED --> [*]
    UNASSIGNED --> CANCELLED : Cancel
    SCHEDULED --> CANCELLED : Cancel
```

### 12.2 Critical Business Rules Implemented in Code

1. **Signature Guard on Job Completion:**
   - When transitioning a work order to `COMPLETED`, `apps.operations.views.WorkOrderViewSet.transition` verifies the presence of an associated `CustomerSignature`.
   - If unsigned, the transition is rejected with `PermissionDenied` unless the acting user has a manager role (`is_manager`: Owner, Admin, Operations, Dispatcher, Finance).
2. **Automated Timestamp Tracking:**
   - Setting status to `ON_SITE` writes `actual_arrival = timezone.now()`.
   - Setting status to `IN_PROGRESS` writes `actual_start = timezone.now()`.
   - Setting status to `COMPLETED` writes `actual_completed = timezone.now()`.
3. **Real-Time Inventory Stock Decrements:**
   - Adding materials to a work order (`POST /api/v1/work-orders/{id}/materials/`) atomically decreases the material's warehouse `stock_quantity`:
     ```python
     material.stock_quantity = material.stock_quantity - item.quantity
     material.save(update_fields=['stock_quantity'])
     ```
4. **Financial Recalculation:**
   - Invoices dynamically aggregate line items:
     $$\text{Subtotal} = \sum (\text{item.quantity} \times \text{item.unit\_price})$$
     $$\text{Total} = \text{Subtotal} - \text{Discount} + \text{Tax}$$
   - When recorded payments equal or exceed `Total`, the status changes to `PAID`; partial payments trigger `PARTIAL`.

---

## 13. Development Commands & Tooling

### 13.1 Backend Commands (`fieldflow-backend/`)

| Command | Description |
| :--- | :--- |
| `python manage.py runserver 8000` | Start local Django HTTP development server. |
| `python manage.py makemigrations` | Detect model changes and generate schema migration files. |
| `python manage.py migrate` | Apply database migrations to active database (SQLite / PostgreSQL). |
| `python manage.py seed_demo` | Generate complete demo organization, technicians, work orders, and parts. |
| `python manage.py createsuperuser` | Create superuser account for Django admin console access. |
| `python manage.py collectstatic --noinput` | Gather static CSS/JS assets into `staticfiles/` directory. |
| `python manage.py check` | Perform static checks on Django configuration and models. |

### 13.2 Frontend Commands (`fieldflow-frontend/`)

| Command | Description |
| :--- | :--- |
| `npm run dev` | Launch Next.js local development server at `http://localhost:3000`. |
| `npm run build` | Compile optimized production build for Next.js App Router. |
| `npm run start` | Serve production build locally. |
| `npm run lint` | Execute ESLint static analysis across TSX components and libraries. |

---

## 14. Testing & Quality Assurance

### 14.1 Current Testing Status
- **Backend:** Models, URL routing, and viewsets conform to Django REST Framework conventions. Automated test suite has basic scaffolding.
- **Frontend:** TypeScript static type checking and ESLint configurations (`eslint-config-next`) are enabled.

### 14.2 Recommended Testing Plan

#### 1. Backend Integration Tests (`pytest-django`)
Create `apps/operations/tests/test_work_orders.py`:
```python
from rest_framework.test import APITestCase
from apps.operations.models import WorkOrder

class WorkOrderTests(APITestCase):
    def test_signature_required_for_technician_completion(self):
        # 1. Authenticate as technician
        # 2. Attempt transition to 'completed' without signature
        # 3. Assert response status is 403 Forbidden
        pass
```

#### 2. End-to-End Tests (Playwright)
Verify end-to-end user workflows:
- Customer request submission &rarr; Dispatch board triage &rarr; Mobile technician completion &rarr; Invoice settlement.

---

## 15. Security & Compliance Controls

1. **Tenant Isolation:** Every operational query is constrained by the resolved tenant membership (`get_current_org`). No tenant can inspect or modify another tenant's records.
2. **Stateless JWT Security:** Access tokens have a 30-minute lifespan with automatic token rotation via SimpleJWT.
3. **HTTP Security Headers:** Configured with `SECURE_BROWSER_XSS_FILTER = True`, `SECURE_CONTENT_TYPE_NOSNIFF = True`, and `X_FRAME_OPTIONS = 'DENY'`.
4. **CORS Governance:** Cross-origin communication is locked to explicitly configured origins (`CORS_ALLOWED_ORIGINS`).
5. **Auditing & Forensics:** Sensitive operational actions (status changes, technician assignments, e-signatures) trigger immutable `AuditLog` records containing IP addresses, user agents, and before/after state diffs.
6. **Input Sanitization:** Django REST Framework serializers enforce field-level validation and typed input boundaries.

---

## 16. Integrations & External Services

| Service Type | Current Implementation | Production Recommendation |
| :--- | :--- | :--- |
| **Relational Database** | PostgreSQL 17 (Docker) / SQLite 3 (Dev) | Managed AWS RDS PostgreSQL or Supabase with automated backups. |
| **Object File Storage** | Local filesystem (`media/work-orders/`) | AWS S3, Cloudflare R2, or Azure Blob Storage with presigned URLs. |
| **Transactional Email** | Local console backend (`DEFAULT_FROM_EMAIL`) | SendGrid, Amazon SES, or Postmark for appointment reminders. |
| **SMS / WhatsApp Alerts** | Not yet implemented | Twilio or Meta WhatsApp Business API for on-site arrival alerts. |
| **Digital Payments** | Manual reconciliation & reference logging | Stripe Billing or UAE-compliant gateways (Telr, Checkout.com, Ziina). |
| **Mapping & Routing** | Lat/Long coordinates stored in database | Google Maps Platform or Mapbox GL for route optimization. |

---

## 17. Docker & Production Deployment

### 17.1 Docker Architecture
The backend includes a production-ready `Dockerfile` and `docker-compose.yml`:
- **API Service:** Python 3.12-slim base with automated migrations and static collection.
- **DB Service:** PostgreSQL 17 Alpine with persistent volume `fieldflow_db`.
- **Media Volume:** Dedicated persistent volume `fieldflow_media` preserving photo uploads and signatures across container restarts.

### 17.2 Production Hardening Checklist
When deploying to AWS, DigitalOcean, GCP, or a private VPS:
- [ ] Set `DJANGO_DEBUG=false` in production environment.
- [ ] Generate a cryptographically secure `DJANGO_SECRET_KEY` (e.g. via `openssl rand -base64 48`).
- [ ] Configure Gunicorn/Uvicorn with Nginx reverse proxy and Let's Encrypt SSL/TLS certificates.
- [ ] Migrate local media storage to S3-compatible cloud object storage.
- [ ] Configure Redis for rate-limiting, caching, and Celery background workers.
- [ ] Establish automated daily database snapshots and off-site backup storage.

---

## 18. Troubleshooting & Frequently Asked Questions

### 18.1 Troubleshooting Common Issues

#### Problem 1: `ValidationError: You do not have access to this organization.`
- **Cause:** Request includes an invalid `X-Organization-ID` header, or the authenticated user does not have an active membership in that organization.
- **Solution:** Verify your memberships via `GET /api/v1/organizations/` or omit the `X-Organization-ID` header to automatically select your primary organization.

#### Problem 2: `PermissionDenied: Customer signature is required before technician completion.`
- **Cause:** A technician attempted to transition a work order directly to `completed` without capturing the customer e-signature.
- **Solution:** Post the customer's signature to `POST /api/v1/work-orders/{id}/signature/` before marking the work order completed, or perform the transition using an Operations Manager or Admin account.

#### Problem 3: Backend defaults to SQLite instead of PostgreSQL.
- **Cause:** `DATABASE_URL` is commented out or missing in `.env`.
- **Solution:** Open `.env` and configure:
  ```env
  DATABASE_URL=postgresql://fieldflow:fieldflow@localhost:5432/fieldflow
  ```

#### Problem 4: CORS Errors on Frontend API Calls.
- **Cause:** Next.js origin is not whitelisted in backend `.env`.
- **Solution:** Add `http://localhost:3000` to `CORS_ALLOWED_ORIGINS` in `fieldflow-backend/.env` and restart the backend.

---

### 18.2 Frequently Asked Questions (FAQ)

**Q: Can I run FieldFlow without Docker or PostgreSQL?**  
A: Yes. The backend detects the absence of `DATABASE_URL` and falls back automatically to SQLite (`db.sqlite3`), enabling zero-dependency local development.

**Q: Are demo accounts pre-configured?**  
A: Yes. Running `python manage.py seed_demo` initializes a superuser/owner account:
- **Username:** `nibras`
- **Password:** `FieldFlow123!`

**Q: How does FieldFlow handle multi-currency operations?**  
A: The `Organization` model defines the operating currency (default `AED`). Invoices, material costs, and dashboard summaries inherit this regional currency setting.

---

## 19. Roadmap & Future Enhancements

### Near-Term
- [ ] **Direct API Integration:** Wire Next.js frontend state to DRF backend endpoints via typed API fetchers.
- [ ] **Automated PDF Generation:** Generate downloadable PDF service reports and invoices with embedded customer e-signatures.
- [ ] **Real-Time WebSocket Updates:** Implement Django Channels / WebSockets for live dispatch board drag-and-drop updates.

### Medium-Term
- [ ] **Geospatial Route Optimization:** Integrate Google Maps / Mapbox for real-time technician GPS tracking and travel route optimization.
- [ ] **Offline PWA Capabilities:** Enable offline checklist completion and signature caching for field technicians in low-connectivity areas.
- [ ] **Payment Gateway Integration:** Direct online invoice payment settlement via Stripe and regional payment processors.

### Long-Term
- [ ] **Predictive Maintenance:** Machine learning models analyzing asset service histories to predict maintenance schedules before equipment failure occurs.
- [ ] **AI-Assisted Dispatch:** Automated scheduling algorithms matching job requirements to technician skill proficiencies, inventory proximity, and traffic conditions.

---

## 20. Contributing & Code Standards

We welcome contributions from the community. Please follow these guidelines:

1. **Fork the Repository:** Create your own branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Coding Standards:**
   - **Backend:** Adhere to PEP 8 standards. Keep business logic encapsulated inside domain services (`apps/*/services.py`) rather than bloated viewsets.
   - **Frontend:** Follow idiomatic Next.js App Router patterns, TypeScript strict typing, and Tailwind CSS best practices.
3. **Commit Conventions:** Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
   ```text
   feat(operations): add GPS tracking coordinates to technician status
   fix(invoices): correct tax recalculation on zero-discount items
   docs(readme): add detailed API curl examples
   ```
4. **Submit a Pull Request:** Provide a clear description of changes, issue references, and verification steps.

---

## 21. License, Credits & Maintainers

### 21.1 License
This project is open-source and licensed under the [MIT License](https://opensource.org/licenses/MIT).

### 21.2 Project Leadership & Maintainers
- **Maintainer:** Nibras & The FieldFlow Engineering Team
- **Project Domain:** Field Service Management (FSM) & Operations SaaS
- **Target Regions:** Middle East (UAE, Saudi Arabia) & Global Enterprise Service Markets

---

<div align="center">
  <sub>Built with care for field service teams everywhere.</sub>
</div>

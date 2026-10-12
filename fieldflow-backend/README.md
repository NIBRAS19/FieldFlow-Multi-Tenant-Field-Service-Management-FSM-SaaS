# FieldFlow Backend

Production-style Django REST backend for the FieldFlow Field Service Management SaaS frontend.

## Included

- JWT authentication
- Multi-tenant organizations
- RBAC memberships
- Customers, locations, assets
- Service requests → work orders
- Scheduling/dispatch data
- Technician profiles and daily jobs
- Checklists, materials, photos/files, customer signatures
- Invoices, invoice items and payments
- Notifications
- Audit logs
- Dashboard and dispatch endpoints
- PostgreSQL or SQLite fallback for local development
- Docker / docker-compose
- Demo seed command

## Local setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env  # macOS/Linux
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  
python manage.py runserver
```

For an instant demo dataset after migrations:

```bash
python manage.py seed_demo
```

Demo user:

- username: `nibras`
- password: `FieldFlow123!`

Change it immediately outside local development.

## Docker

```bash
docker compose up --build
```

Then run the seed command in another terminal:

```bash
docker compose exec api python manage.py seed_demo
```

## API base

`http://localhost:8000/api/v1/`

All authenticated organization endpoints accept:

`X-Organization-ID: <organization id>`

If omitted, the user's first active organization is selected.

## Authentication

### Register

`POST /api/v1/auth/register/`

```json
{
  "username": "owner",
  "first_name": "Owner",
  "last_name": "User",
  "email": "owner@example.com",
  "password": "StrongPassword123!",
  "phone": "+971500000000",
  "organization_name": "Example Services LLC"
}
```

### Login

`POST /api/v1/auth/login/`

```json
{
  "username": "nibras",
  "password": "FieldFlow123!"
}
```

Use the returned `access` token as:

`Authorization: Bearer <access-token>`

## Important production hardening

Before production deployment, add:

- HTTPS and secure cookies/token storage strategy
- object-storage uploads (S3-compatible) rather than local disk
- malware/file scanning for uploads
- background task queue for email/PDF work
- transactional email provider
- Redis for caching/realtime/background jobs
- stricter CORS/ALLOWED_HOSTS
- secret management
- API throttling and WAF
- database backups and migration automation
- proper observability/error tracking
- automated test suite and CI/CD

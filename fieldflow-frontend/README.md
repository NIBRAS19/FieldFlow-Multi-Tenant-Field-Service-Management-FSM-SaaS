# FieldFlow Frontend

A frontend-only Field Service Management SaaS prototype based on the FieldFlow PRD.

## Included
- Premium responsive Next.js App Router UI
- Operations dashboard
- Service requests
- Work orders
- Schedule
- Dispatch board
- Customers
- Technicians
- Assets
- Invoices
- Reports
- Settings / security posture
- Customer portal
- Technician mobile workflow
- Mock data only; no paid API is required

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:3000

Routes:
- `/` landing page
- `/app/dashboard` operations console
- `/app/requests`
- `/app/work-orders`
- `/app/schedule`
- `/app/dispatch`
- `/app/customers`
- `/app/technicians`
- `/app/assets`
- `/app/invoices`
- `/app/reports`
- `/app/settings`
- `/portal` customer portal
- `/technician` technician mobile view

## Next implementation steps
Connect these screens to Django REST Framework / PostgreSQL, then add authentication, tenant isolation, real persistence, file uploads, notifications, background jobs, and optional local AI through Ollama.

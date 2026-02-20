# Cultivar

SvelteKit + FastAPI SaaS application template. Generated from saas-template-svelte-fastapi.

## Quick Start

### Local Development (with Docker)

```bash
cp .env.example .env
# Edit .env with your values
docker compose -f docker-compose.dev.yml up
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development (native)

```bash
# Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

### Vagrant Dev VM

If using the OpenClaw dev environment:

```bash
cd ~/dev-environment
vagrant up
vagrant ssh
cd ~/projects/cultivar-saas
# Then run docker compose or native commands as above
```

## Stack

- **Frontend:** SvelteKit, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Cache:** Redis

## CI/CD

This repo includes the OpenClaw agent pipeline. Configure GitHub secrets:
- `DEPLOY_SSH_KEY` - SSH private key
- `STAGING_HOST` - AWS VPS hostname/IP (or use `AWS_STAGING_HOST`)
- `DEPLOY_USER` - Deploy user

# Deploy Dashboard Port to Cultivar

The OpenClaw Greenhouse dashboard has been ported to Cultivar SaaS. Follow these steps to deploy.

## Pre-deploy checklist

- [x] Dashboard layout with sidebar, breadcrumbs, theme switching
- [x] Overview, Create Idea, Idea Garden, Gardeners, Org Chart modules
- [x] Backend: Initiative, Goal, Task CRUD; Agent model; dashboard overview, org-tree, apply-plan
- [x] Alembic migration for agents table

## Database migration

If the database already exists, run Alembic to add the `agents` table:

```bash
cd backend
alembic upgrade head
```

For fresh installs, `init_db()` (run on startup) creates all tables including `agents`.

## Deploy steps

1. Push to GitHub
2. SSH to AWS VPS
3. Pull latest: `cd /path/to/cultivar-saas && git pull`
4. Rebuild and restart:
   ```bash
   docker-compose -f docker-compose.staging.yml build --no-cache
   docker-compose -f docker-compose.staging.yml up -d
   ```
5. If needed, run migrations inside the backend container:
   ```bash
   docker exec cultivar-saas_backend_staging alembic upgrade head
   ```

## Verify

- Visit cultivar.life
- Log in
- Dashboard should show: Overview, Create idea/seed, Idea Garden, Gardeners, Org Chart in the sidebar
- Create an idea, generate a plan, apply it
- View ideas in Idea Garden and the org tree in Org Chart

"""Dashboard API - overview, org-tree."""
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.goal import Goal
from app.models.idea import Idea
from app.models.initiative import Initiative
from app.models.task import Task

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
def get_overview(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return counts for dashboard overview (ideas, initiatives, goals, tasks, task status)."""
    ideas_count = db.query(func.count(Idea.id)).filter(Idea.user_id == user_id).scalar() or 0
    initiatives_count = db.query(func.count(Initiative.id)).filter(Initiative.user_id == user_id).scalar() or 0
    goals_count = (
        db.query(func.count(Goal.id))
        .join(Initiative)
        .filter(Initiative.user_id == user_id)
        .scalar()
        or 0
    )
    tasks_count = (
        db.query(func.count(Task.id))
        .join(Initiative)
        .filter(Initiative.user_id == user_id)
        .scalar()
        or 0
    )

    # Task status counts
    task_status = (
        db.query(Task.status, func.count(Task.id))
        .join(Initiative)
        .filter(Initiative.user_id == user_id)
        .group_by(Task.status)
        .all()
    )
    status_map = {row[0]: row[1] for row in task_status}

    return {
        "counts": {
            "ideas": ideas_count,
            "initiatives": initiatives_count,
            "goals": goals_count,
            "tasks": tasks_count,
        },
        "taskStatus": {
            "planned": status_map.get("planned", 0),
            "approved": status_map.get("approved", 0),
            "running": status_map.get("running", 0),
            "completed": status_map.get("completed", 0),
        },
    }


@router.get("/org-tree")
def get_org_tree(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return nested initiative -> goals -> tasks hierarchy for org chart."""
    initiatives = (
        db.query(Initiative)
        .filter(Initiative.user_id == user_id)
        .order_by(Initiative.created_at.desc())
        .all()
    )
    result: list[dict[str, Any]] = []
    for init in initiatives:
        goals_list = (
            db.query(Goal)
            .filter(Goal.initiative_id == init.id)
            .order_by(Goal.created_at.desc())
            .all()
        )
        goals_data: list[dict[str, Any]] = []
        for g in goals_list:
            tasks_list = (
                db.query(Task)
                .filter(Task.goal_id == g.id)
                .order_by(Task.created_at.desc())
                .all()
            )
            goals_data.append({
                "id": g.id,
                "title": g.title,
                "status": g.status,
                "tasks": [
                    {"id": t.id, "title": t.title, "status": t.status}
                    for t in tasks_list
                ],
            })
        # Include tasks with no goal
        orphan_tasks = (
            db.query(Task)
            .filter(Task.initiative_id == init.id, Task.goal_id.is_(None))
            .order_by(Task.created_at.desc())
            .all()
        )
        for t in orphan_tasks:
            goals_data.append({
                "id": None,
                "title": "(Unassigned)",
                "status": "",
                "tasks": [{"id": t.id, "title": t.title, "status": t.status}],
            })
        result.append({
            "id": init.id,
            "name": init.name,
            "ideaId": init.idea_id,
            "status": init.status,
            "priority": init.priority,
            "goals": goals_data,
        })
    return {"initiatives": result}

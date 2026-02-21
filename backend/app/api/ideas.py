"""Ideas (seeds) CRUD API."""
import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.goal import Goal
from app.models.idea import Idea
from app.models.initiative import Initiative
from app.models.task import Task

router = APIRouter(prefix="/ideas", tags=["ideas"])


class IdeaCreate(BaseModel):
    title: str
    description: Optional[str] = None
    tags: list[str] = []


class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None


class IdeaResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    tags: list[str]
    status: str

    class Config:
        from_attributes = True


class ApplyPlanRequest(BaseModel):
    plan_markdown: str


def _parse_plan_markdown(plan_md: str) -> tuple[list[str], list[dict]]:
    """Extract goals and tasks from plan markdown. Returns (goals, tasks)."""
    goals: list[str] = []
    tasks: list[dict] = []
    lines = plan_md.splitlines()
    section: str | None = None

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        lower = line_stripped.lower()
        if "goal" in lower and (line.startswith("#") or line.startswith("##")):
            section = "goals"
            continue
        if "task" in lower and (line.startswith("#") or line.startswith("##")):
            section = "tasks"
            continue

        if section == "goals" and (line_stripped.startswith("-") or (line_stripped and line_stripped[0].isdigit())):
            text = re.sub(r"^[-*\s]*\d*[.)]\s*", "", line_stripped).strip()
            if text:
                goals.append(text)
        elif section == "tasks" and ("[ ]" in line_stripped or "[x]" in line_stripped.lower()):
            text = line_stripped.split("]", 1)[-1].strip()
            est: float | None = None
            if "(est:" in text.lower():
                parts = text.rsplit("(", 1)
                text = parts[0].strip()
                est_part = parts[1].rstrip(")")
                m = re.search(r"[\d.]+", est_part)
                if m:
                    try:
                        est = float(m.group())
                    except ValueError:
                        pass
            tasks.append({"title": text, "estimate_hours": est})

    return goals, tasks


@router.post("/{idea_id}/apply-plan")
def apply_plan(
    idea_id: str,
    data: ApplyPlanRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Create initiative, goals, and tasks from a generated plan markdown."""
    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    goals_text, tasks_data = _parse_plan_markdown(data.plan_markdown or "")

    initiative = Initiative(
        user_id=user_id,
        idea_id=idea_id,
        name=f"Plan: {idea.title[:100]}",
        status="planning",
        priority="medium",
    )
    db.add(initiative)
    db.flush()

    goal_ids: list[str] = []
    for gtext in goals_text:
        goal = Goal(initiative_id=initiative.id, title=gtext[:512], status="planned")
        db.add(goal)
        db.flush()
        goal_ids.append(goal.id)

    for t in tasks_data:
        goal_id = goal_ids[0] if goal_ids else None
        task = Task(
            initiative_id=initiative.id,
            goal_id=goal_id,
            title=t["title"][:512],
            estimate_hours=t.get("estimate_hours"),
            status="planned",
            risk_level="medium",
        )
        db.add(task)

    db.commit()
    return {"initiativeId": initiative.id, "goalsCreated": len(goals_text), "tasksCreated": len(tasks_data)}


@router.get("", response_model=list[IdeaResponse])
def list_ideas(
    status: Optional[str] = None,
    tag: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    q = db.query(Idea).filter(Idea.user_id == user_id)
    if status:
        q = q.filter(Idea.status == status)
    if tag:
        q = q.filter(Idea.tags.contains([tag]))
    ideas = q.order_by(Idea.created_at.desc()).all()
    return ideas


@router.post("", response_model=IdeaResponse)
def create_idea(
    data: IdeaCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    idea = Idea(
        user_id=user_id,
        title=data.title,
        description=data.description,
        tags=data.tags or [],
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea


@router.get("/{idea_id}", response_model=IdeaResponse)
def get_idea(
    idea_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.patch("/{idea_id}", response_model=IdeaResponse)
def update_idea(
    idea_id: str,
    data: IdeaUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if data.title is not None:
        idea.title = data.title
    if data.description is not None:
        idea.description = data.description
    if data.tags is not None:
        idea.tags = data.tags
    if data.status is not None:
        idea.status = data.status
    db.commit()
    db.refresh(idea)
    return idea


@router.delete("/{idea_id}", status_code=204)
def delete_idea(
    idea_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    db.delete(idea)
    db.commit()

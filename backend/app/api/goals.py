"""Goals CRUD API."""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.goal import Goal
from app.models.initiative import Initiative

router = APIRouter(prefix="/goals", tags=["goals"])


class GoalCreate(BaseModel):
    initiative_id: str
    title: str
    metric: Optional[str] = None
    target: Optional[str] = None
    due_at: Optional[date] = None
    status: str = "planned"


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    metric: Optional[str] = None
    target: Optional[str] = None
    due_at: Optional[date] = None
    status: Optional[str] = None


class GoalResponse(BaseModel):
    id: str
    initiative_id: str
    title: str
    metric: Optional[str]
    target: Optional[str]
    due_at: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True


def _serialize(g: Goal) -> dict:
    return {
        "id": g.id,
        "initiative_id": g.initiative_id,
        "title": g.title,
        "metric": g.metric,
        "target": g.target,
        "due_at": g.due_at.isoformat() if g.due_at else None,
        "status": g.status,
        "created_at": g.created_at.isoformat() if g.created_at else None,
    }


def _user_owns_initiative(db: Session, user_id: str, initiative_id: str) -> bool:
    return db.query(Initiative).filter(Initiative.id == initiative_id, Initiative.user_id == user_id).first() is not None


@router.get("", response_model=list[GoalResponse])
def list_goals(
    initiative_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    q = db.query(Goal).join(Initiative).filter(Initiative.user_id == user_id)
    if initiative_id:
        q = q.filter(Goal.initiative_id == initiative_id)
    goals = q.order_by(Goal.created_at.desc()).all()
    return [_serialize(g) for g in goals]


@router.post("", response_model=GoalResponse)
def create_goal(
    data: GoalCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if not _user_owns_initiative(db, user_id, data.initiative_id):
        raise HTTPException(status_code=404, detail="Initiative not found")
    goal = Goal(
        initiative_id=data.initiative_id,
        title=data.title,
        metric=data.metric,
        target=data.target,
        due_at=data.due_at,
        status=data.status,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return _serialize(goal)


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    goal = db.query(Goal).join(Initiative).filter(Goal.id == goal_id, Initiative.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _serialize(goal)


@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: str,
    data: GoalUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    goal = db.query(Goal).join(Initiative).filter(Goal.id == goal_id, Initiative.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if data.title is not None:
        goal.title = data.title
    if data.metric is not None:
        goal.metric = data.metric
    if data.target is not None:
        goal.target = data.target
    if data.due_at is not None:
        goal.due_at = data.due_at
    if data.status is not None:
        goal.status = data.status
    db.commit()
    db.refresh(goal)
    return _serialize(goal)


@router.delete("/{goal_id}", status_code=204)
def delete_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    goal = db.query(Goal).join(Initiative).filter(Goal.id == goal_id, Initiative.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()

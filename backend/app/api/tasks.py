"""Tasks CRUD API."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.task import Task
from app.models.initiative import Initiative

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    initiative_id: str
    goal_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    risk_level: str = "low"
    status: str = "planned"
    estimate_hours: Optional[float] = None


class TaskUpdate(BaseModel):
    goal_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None
    estimate_hours: Optional[float] = None


class TaskResponse(BaseModel):
    id: str
    initiative_id: str
    goal_id: Optional[str]
    title: str
    description: Optional[str]
    owner: Optional[str]
    risk_level: str
    status: str
    estimate_hours: Optional[float]
    created_at: str

    class Config:
        from_attributes = True


def _serialize(t: Task) -> dict:
    return {
        "id": t.id,
        "initiative_id": t.initiative_id,
        "goal_id": t.goal_id,
        "title": t.title,
        "description": t.description,
        "owner": t.owner,
        "risk_level": t.risk_level,
        "status": t.status,
        "estimate_hours": t.estimate_hours,
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }


def _user_owns_initiative(db: Session, user_id: str, initiative_id: str) -> bool:
    return db.query(Initiative).filter(Initiative.id == initiative_id, Initiative.user_id == user_id).first() is not None


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    initiative_id: Optional[str] = None,
    goal_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    q = db.query(Task).join(Initiative).filter(Initiative.user_id == user_id)
    if initiative_id:
        q = q.filter(Task.initiative_id == initiative_id)
    if goal_id:
        q = q.filter(Task.goal_id == goal_id)
    tasks = q.order_by(Task.created_at.desc()).all()
    return [_serialize(t) for t in tasks]


@router.post("", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if not _user_owns_initiative(db, user_id, data.initiative_id):
        raise HTTPException(status_code=404, detail="Initiative not found")
    task = Task(
        initiative_id=data.initiative_id,
        goal_id=data.goal_id,
        title=data.title,
        description=data.description,
        owner=data.owner,
        risk_level=data.risk_level,
        status=data.status,
        estimate_hours=data.estimate_hours,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _serialize(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(Task).join(Initiative).filter(Task.id == task_id, Initiative.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return _serialize(task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(Task).join(Initiative).filter(Task.id == task_id, Initiative.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if data.goal_id is not None:
        task.goal_id = data.goal_id
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.owner is not None:
        task.owner = data.owner
    if data.risk_level is not None:
        task.risk_level = data.risk_level
    if data.status is not None:
        task.status = data.status
    if data.estimate_hours is not None:
        task.estimate_hours = data.estimate_hours
    db.commit()
    db.refresh(task)
    return _serialize(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(Task).join(Initiative).filter(Task.id == task_id, Initiative.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

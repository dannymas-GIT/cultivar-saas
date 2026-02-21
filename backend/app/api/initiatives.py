"""Initiatives CRUD API."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.initiative import Initiative
from app.models.idea import Idea

router = APIRouter(prefix="/initiatives", tags=["initiatives"])


class InitiativeCreate(BaseModel):
    idea_id: str
    name: str
    owner: Optional[str] = None
    status: str = "planning"
    priority: str = "medium"


class InitiativeUpdate(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class InitiativeResponse(BaseModel):
    id: str
    user_id: str
    idea_id: str
    name: str
    owner: Optional[str]
    status: str
    priority: str
    created_at: str

    class Config:
        from_attributes = True


def _serialize(init: Initiative) -> dict:
    return {
        "id": init.id,
        "user_id": init.user_id,
        "idea_id": init.idea_id,
        "name": init.name,
        "owner": init.owner,
        "status": init.status,
        "priority": init.priority,
        "created_at": init.created_at.isoformat() if init.created_at else None,
    }


@router.get("", response_model=list[InitiativeResponse])
def list_initiatives(
    idea_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    q = db.query(Initiative).filter(Initiative.user_id == user_id)
    if idea_id:
        q = q.filter(Initiative.idea_id == idea_id)
    initiatives = q.order_by(Initiative.created_at.desc()).all()
    return [_serialize(i) for i in initiatives]


@router.post("", response_model=InitiativeResponse)
def create_initiative(
    data: InitiativeCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    idea = db.query(Idea).filter(Idea.id == data.idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    init = Initiative(
        user_id=user_id,
        idea_id=data.idea_id,
        name=data.name,
        owner=data.owner,
        status=data.status,
        priority=data.priority,
    )
    db.add(init)
    db.commit()
    db.refresh(init)
    return _serialize(init)


@router.get("/{initiative_id}", response_model=InitiativeResponse)
def get_initiative(
    initiative_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    init = db.query(Initiative).filter(Initiative.id == initiative_id, Initiative.user_id == user_id).first()
    if not init:
        raise HTTPException(status_code=404, detail="Initiative not found")
    return _serialize(init)


@router.patch("/{initiative_id}", response_model=InitiativeResponse)
def update_initiative(
    initiative_id: str,
    data: InitiativeUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    init = db.query(Initiative).filter(Initiative.id == initiative_id, Initiative.user_id == user_id).first()
    if not init:
        raise HTTPException(status_code=404, detail="Initiative not found")
    if data.name is not None:
        init.name = data.name
    if data.owner is not None:
        init.owner = data.owner
    if data.status is not None:
        init.status = data.status
    if data.priority is not None:
        init.priority = data.priority
    db.commit()
    db.refresh(init)
    return _serialize(init)


@router.delete("/{initiative_id}", status_code=204)
def delete_initiative(
    initiative_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    init = db.query(Initiative).filter(Initiative.id == initiative_id, Initiative.user_id == user_id).first()
    if not init:
        raise HTTPException(status_code=404, detail="Initiative not found")
    db.delete(init)
    db.commit()

"""Ideas (seeds) CRUD API."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import decode_token
from app.core.database import get_db
from app.models.idea import Idea

router = APIRouter(prefix="/ideas", tags=["ideas"])


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth")
    token = authorization.split(" ", 1)[1]
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


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


@router.get("", response_model=list[IdeaResponse])
def list_ideas(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    ideas = db.query(Idea).filter(Idea.user_id == user_id).order_by(Idea.created_at.desc()).all()
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

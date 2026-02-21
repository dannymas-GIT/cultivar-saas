"""Agents (gardeners) CRUD API."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.models.agent import Agent

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentCreate(BaseModel):
    name: str
    role: str = "gardener"
    description: Optional[str] = None
    status: str = "active"


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True


def _serialize(a: Agent) -> dict:
    return {
        "id": a.id,
        "name": a.name,
        "role": a.role,
        "description": a.description,
        "status": a.status,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.get("", response_model=list[AgentResponse])
def list_agents(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    agents = db.query(Agent).filter(Agent.user_id == user_id).order_by(Agent.created_at.desc()).all()
    return [_serialize(a) for a in agents]


@router.post("", response_model=AgentResponse)
def create_agent(
    data: AgentCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    agent = Agent(
        user_id=user_id,
        name=data.name,
        role=data.role,
        description=data.description,
        status=data.status,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return _serialize(agent)


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.user_id == user_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return _serialize(agent)


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: str,
    data: AgentUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.user_id == user_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if data.name is not None:
        agent.name = data.name
    if data.role is not None:
        agent.role = data.role
    if data.description is not None:
        agent.description = data.description
    if data.status is not None:
        agent.status = data.status
    db.commit()
    db.refresh(agent)
    return _serialize(agent)


@router.delete("/{agent_id}", status_code=204)
def delete_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.user_id == user_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()

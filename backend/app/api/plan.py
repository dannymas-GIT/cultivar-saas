"""Planning endpoint - calls planning-agent skill."""
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import get_current_user_id
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/plan", tags=["plan"])


class PlanRequest(BaseModel):
    idea: str


class PlanResponse(BaseModel):
    plan_markdown: str
    status: str = "OK"


@router.post("", response_model=PlanResponse)
def create_plan(
    data: PlanRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Generate a structured plan from idea text using planning-agent skill."""
    script = Path("/opt/projects/workspace/skills/planning-agent/scripts/plan.py")
    if not script.exists():
        script = Path(os.environ.get("OPENCLAW_WORKSPACE", "")) / "skills/planning-agent/scripts/plan.py"
    if not script.exists():
        raise HTTPException(
            status_code=503,
            detail="Planning agent not available. Set OPENCLAW_WORKSPACE or install planning-agent skill.",
        )
    env = os.environ.copy()
    env_file = Path.home() / ".openclaw" / "openclaw.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    try:
        result = subprocess.run(
            [os.environ.get("PYTHON", "python3"), str(script), "--idea", data.idea, "--format", "json"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(script.parent),
            env=env,
        )
        out = result.stdout or result.stderr or ""
        data_out = json.loads(out)
        if data_out.get("status") == "SKIP":
            raise HTTPException(status_code=503, detail=data_out.get("error", "Planning agent unavailable"))
        if data_out.get("status") == "FAIL":
            raise HTTPException(status_code=500, detail=data_out.get("error", "Planning failed"))
        return PlanResponse(plan_markdown=data_out.get("plan_markdown", ""))
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Planning request timed out")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid planning agent response")

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Job
from app.auth import get_current_user
from app.tasks import square_sum, cube_sum
from app.utils.rate_limiter import limiter

router = APIRouter()
def get_session_local():
    yield SessionLocal()
@router.post("/jobs")
@limiter.limit("20/minute")
def submit_job(request: Request, data: list[int], operation: str, db: Session = Depends(get_session_local), current_user=Depends(get_current_user)):
    job = Job(data=str(data), operation=operation, status="PENDING", owner_id=current_user.id)
    db.add(job)
    db.commit()
    task = square_sum.delay(data, job.id) if operation == "square_sum" else cube_sum.delay(data, job.id)
    job.status = "IN_PROGRESS"
    db.commit()
    return {"job_id": job.id, "status": job.status}

@router.get("/jobs/{job_id}/status")
@limiter.limit("30/minute")
def check_status(request: Request, job_id: int, db: Session = Depends(get_session_local), current_user=Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": job.status}

@router.get("/jobs/{job_id}/result")
@limiter.limit("30/minute")
def get_result(request: Request, job_id: int, db: Session = Depends(get_session_local), current_user=Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": job.result} if job.status == "SUCCESS" else {"message": "Still processing..."}
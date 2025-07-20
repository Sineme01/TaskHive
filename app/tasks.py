from celery import Celery
import os
import json
from dotenv import load_dotenv
from app.db import SessionLocal
from app.models import Job

load_dotenv()

celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

@celery.task(name='square_sum')
def square_sum(data, job_id):
    result = sum([x**2 for x in data])
    
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "SUCCESS"
        job.result = str(result)
        db.commit()
        db.close()
    
    return result

@celery.task(name='cube_sum')
def cube_sum(data, job_id):
    result = sum([x**3 for x in data])

    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "SUCCESS"
        job.result = str(result)
        db.commit()
        db.close()

    return result
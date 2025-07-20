from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from app.auth import get_password_hash, authenticate_user, create_access_token
from app.utils.rate_limiter import limiter

router = APIRouter()

def get_session_local():
    yield SessionLocal()

@router.post("/register")
@limiter.limit("5/minute")
def register_user(
    request: Request,  # Required for rate limiter to access IP
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_session_local)
):
    # Check if user exists
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Create user
    user = User(
        username=username,
        email=email,
        hashed_password=get_password_hash(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

@router.post("/login")
@limiter.limit("10/minute")
def login(
    request: Request,  # Required for rate limiter to access IP
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session_local)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

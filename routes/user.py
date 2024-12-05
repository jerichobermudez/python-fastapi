import models
import schemas
import utils
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.post(
    '/register',
    status_code = status.HTTP_201_CREATED,
    response_model = schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    email_exists = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if email_exists:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Email already exists!'
        )

    username_exists = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if username_exists:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Username already exists!'
        )

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump(exclude = { 'confirm_password' }))
    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user


@router.get('/users/{id}', response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'User not found'
        )
    
    return user
import database
import models
import utils
from . import oauth2
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

router = APIRouter(tags = ['Authentication'])

@router.post('/login')
def login(
    input: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        or_(
            models.User.username == input.username,
            models.User.email == input.username
        )
    ).first()

    if not user or not utils.verify(input.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'Invalid Credentials'
        )
    
    token = oauth2.generate_token(data = { 'id': user.id })

    user.token = token
    db.commit()

    return {
        'id': user.id,
        'token': token
    }

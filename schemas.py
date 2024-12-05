import re
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from fastapi import status, HTTPException
from typing import List

COMMON_PASSWORDS = [
    'Pa$$w0rd',
    'p@ssw0rd',
    'p@ssword',
    '11223344',
    'password',
    '123456',
    'qwerty'
]

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    username: str
    password: str
    confirm_password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must have at least one lowercase letter.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must have at least one uppercase letter.')
        if not re.search(r'\d', v):
            raise ValueError('Password must have at least one number.')
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('Password must have at least one special character.')

        if v in COMMON_PASSWORDS:
            raise ValueError('Please choose a stronger password.')

        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = 'Passwords do not match!'
            )

        return v

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Custom error format for validation
class ValidationErrorDetail(BaseModel):
    field: str
    message: str

class CustomValidationErrorResponse(BaseModel):
    errors: List[ValidationErrorDetail]
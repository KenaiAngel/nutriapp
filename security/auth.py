from datetime import timedelta, datetime, timezone
# Annotated allows combining type hints and FastAPI dependencies
from typing import Annotated  
# FastAPI tools for creating routes, handling dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException

# Pydantic BaseModel — used for defining request/response schemas
from pydantic import BaseModel
# SQLAlchemy Session — used to interact with the database
from sqlalchemy.orm import Session

# HTTP status codes (e.g., 200, 401, 201)
from starlette import status
# Password hashing context from Passlib (handles password encryption)
from passlib.context import CryptContext

# FastAPI’s OAuth2 utilities for authentication
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# JSON Web Token (JWT) tools for encoding/decoding tokens
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

from domain.users import add_user, authenticate_user
from security.encrypt import create_access_token

load_dotenv()


router = APIRouter(
    prefix='/auth',       # Every route here will start with /auth
    tags=['auth']         
)
class CreateUserRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request:CreateUserRequest):
    add_user(create_user_request)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print('Entre a post 1ro ', form_data)
    user = authenticate_user(form_data.username, form_data.password)
    print('Post 2do ', user)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )
    
    token = create_access_token(user.mail, user.id, user.role,timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

    



# JSON Web Token (JWT) tools for encoding/decoding tokens
from jose import jwt, JWTError
# Password hashing context from Passlib (handles password encryption)
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
# Annotated allows combining type hints and FastAPI dependencies
from typing import Annotated  
# FastAPI tools for creating routes, handling dependencies, and exceptions
from fastapi import Depends, HTTPException
# FastAPI’s OAuth2 utilities for authentication
from fastapi.security import  OAuth2PasswordBearer
# HTTP status codes (e.g., 200, 401, 201)
from starlette import status



import os
from dotenv import load_dotenv

load_dotenv()
# Defines how the app extracts the token (from Authorization header)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = os.getenv("SECRET_KEY", "SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

bcrypt_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')


def hash_password (pre_pass):
    print('Contrasena sin hash: ', pre_pass)
    hash = bcrypt_context.hash(pre_pass)
    print('Contrasena hasheada: ', hash)
    return  hash

def verify_password(db_pass, current_pass):
    print('ENTREEEEEEEEEEE')
    print("Validacion: ",bcrypt_context.verify(current_pass,db_pass))
    return bcrypt_context.verify(current_pass,db_pass)


# ---------- JWT CREATION ----------

# Creates a signed JWT token containing username and id
def create_access_token(mail: str, user_id: int, role: str, expires_delta: timedelta):
    # Basic payload with user info
    encode = {'sub': mail, 'id': user_id, 'role':role}
    
    # Expiration time
    expires = datetime.now(timezone.utc) + expires_delta  
    
    # Add expiration claim to token payload
    encode.update({'exp': expires})
    
    # Encode and sign the JWT using the secret key and algorithm
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------- JWT VALIDATION ----------

# Extracts and verifies current user based on provided JWT
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # Decode the token (verify signature and expiration)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract data from token payload
        mail: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: int = payload.get('role')

        # If missing or invalid → unauthorized
        if mail is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user.'
            )

        # Return a dict representing the authenticated user
        return {'mail': mail, 'id': user_id, 'role': role}

    # If decoding fails (bad signature, expired token, etc.)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user.'
        )

user_dependency = Annotated[dict,Depends(get_current_user)]

from models.connection import DBManager
from models.models_db import User
from pydantic import BaseModel
from security.encrypt import hash_password, verify_password
from typing import Optional

class CreatenNutriRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    password: str
    license: int 


def add_user(create_user_model: CreatenNutriRequest, nutri_id: Optional[int] = None):

    with DBManager() as db:
        hashed = hash_password(create_user_model.password)

        # Caso: se está creando un PACIENTE asignado a un nutriólogo
        if nutri_id is not None:
            create_user = User(
                name=create_user_model.name,
                first_name=create_user_model.first_name,
                last_name=create_user_model.last_name,
                mail=create_user_model.mail,
                hashed_password=hashed,
                nutriologist_id=nutri_id,
                role='PACIENTE'
            )

        # Caso: se está creando un NUTRIÓLOGO
        else:
            if create_user_model.license != 12345678:
                return {
                    'valid': False,
                    'message': 'Forbidden Access'
                }
            
            create_user = User(
                name=create_user_model.name,
                first_name=create_user_model.first_name,
                last_name=create_user_model.last_name,
                mail=create_user_model.mail,
                hashed_password=hashed,
                role='NUTRIOLOGO'
            )

        db.add(create_user)
        db.commit()

        return {
            'valid': True,
            'message': 'Access'
        }

def authenticate_user(mail: str, password: str):
    with DBManager() as db:
        user = db.query(User).filter(User.mail == mail).first()
        if not user: 
            return False
        # Verifies that the password matches the stored hashed password
        if not verify_password(user.hashed_password,password):
            return False
        return user

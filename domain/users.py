from models.connection import DBManager
from models.models_db import User
from pydantic import BaseModel
from security.encrypt import hash_password, verify_password
from typing import Optional
from datetime import date

class CreatenNutriRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    password: str
    license: int 

class CreatenPacienteRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    age: int
    gender: str
    phone: str 
    height: float | None
    actual_weight: float | None
    goal_weight:float | None
    last_visit:date
    password: str

def add_paci (create_user_model: CreatenPacienteRequest, nutri_id:int):
    with DBManager() as db:
        hashed = hash_password(create_user_model.password)
        create_user = User(
            name=create_user_model.name,
            first_name=create_user_model.first_name,
            last_name=create_user_model.last_name,
            mail=create_user_model.mail,
            age= create_user_model.age,
            gender = create_user_model.gender,
            cellphone = create_user_model.phone,
            height = create_user_model.height,
            actual_weight = create_user_model.actual_weight,
            goal_weight = create_user_model.actual_weight,
            last_visit= create_user_model.last_visit, 
            hashed_password=hashed,
            nutriologist_id=nutri_id,
            role='PACIENTE'
        )
        db.add(create_user)
        db.commit()
        db.refresh(create_user)

        user = {    
            'id': create_user.id,
            'name':create_user.name,
            'first_name':create_user.first_name,
            'last_name':create_user.last_name,
            'mail':create_user.mail,
            'age': create_user.age,
            'gender': create_user.gender,
            'cellphone':  create_user.cellphone,
            'height': create_user.height,
            'actual_weight':create_user.actual_weight,
            'goal_weight':create_user.actual_weight,
            'last_visit': create_user.last_visit, 
        }

        return {
            'valid': True,
            'message': 'Access',
            'user': user
        }


def add_nutri(create_user_model: CreatenNutriRequest):

    with DBManager() as db:
        hashed = hash_password(create_user_model.password)


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

def get_general_user_info(user_id:int):
    with DBManager() as db:
        u = db.query(User).filter(User.id == user_id).first()

        return {
            'mail': u.mail,
            'name': u.name,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'role': u.role,
            "id": u.id,
            "mail": u.mail,
            "age": u.age,
            "height": u.height,
            "goal_weight": u.goal_weight,
            "actual_weight": u.actual_weight,
            "gender": u.gender,
            "cellphone": u.cellphone,
            "last_visit": u.last_visit
        }
from models.connection import DBManager
from models.models_db import Users
from pydantic import BaseModel
from security.encrypt import hash_password, verify_password

class CreateUserRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    password: str
    role: str

def add_user(create_user_model: CreateUserRequest):
    with DBManager() as db:  # La sesión se abre y se cierra automáticamente
        hash = hash_password(create_user_model.password) 
        print("Contrasena a guardar: ", hash)
        # Create a new user model instance with a hashed password
        create_user = Users(
            name=create_user_model.name,
            first_name= create_user_model.first_name,
            last_name= create_user_model.last_name,
            mail= create_user_model.mail,
            hashed_password= hash,
            role = create_user_model.role
        )
        db.add(create_user)
        db.commit()

def authenticate_user(mail: str, password: str):
    with DBManager() as db:
        user = db.query(Users).filter(Users.mail == mail).first()
        if not user: 
            return False
        # Verifies that the password matches the stored hashed password
        if not verify_password(user.hashed_password,password):
            return False
        return user

from models.connection import DBManager
from models.models_db import Users, Foods, Food_Groups
from pydantic import BaseModel

def get_all_food_by_id_nutriologist(nutriologist_id: int, patient_id: int):
    with DBManager() as db:
        foods = db.query(Foods).filter(
            (Foods.nutriologist_id == nutriologist_id) & (Foods.patient_id == patient_id)
        ).all()
        return foods
    
def get_patients(nutriologist_id: int):
    with DBManager() as db:
        foods = db.query(Users).filter(Users.nutriologist_id == nutriologist_id).all()
        return foods
    
def add_patient(patient_id: int, nutri_id: int):
    with DBManager() as db:
        # Buscar al paciente por su ID
        patient = db.query(Users).filter(Users.id == patient_id).first()

        if not patient:
            raise ValueError("Paciente no encontrado")

        # Actualizar el nutriologist_id
        patient.nutriologist_id = nutri_id

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(patient)

        return patient

class CreateFoodGroupRequest(BaseModel):
    food_id:int
    group_name: str
    description: str
    kcal: float
    protein: float
    carbohydrates: float
    fats: float


def add_food_group(current_food_group:CreateFoodGroupRequest):
    with DBManager() as db:
        new_food_group = Food_Groups(
            group_name = current_food_group.group_name,
            description = current_food_group.description,
            kcal = current_food_group.kcal,
            protein = current_food_group.protein,
            carbohydrates= current_food_group.carbohydrates,
            fats= current_food_group.fats,
            food_id= current_food_group.food_id
        )
        db.add(new_food_group)
        db.commit()
        print("Database food group: ",new_food_group)
        return new_food_group

def get_all_food_groups_associate_food(food_id: int):
    with DBManager() as db:
        foods = db.query(Food_Groups).filter(Food_Groups.food_id == food_id).all()
        return foods
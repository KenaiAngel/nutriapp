from models.connection import DBManager
from models.models_db import Users, Foods, Food_Groups
from pydantic import BaseModel

def get_all_food_by_id_nutriologist(nutriologist_id: int, patient_id: int):
    with DBManager() as db:
        food_event = db.query(Food_Event).filter(
            (Food_Event.nutriologist_id == nutriologist_id) & (Food_Event.patient_id == patient_id)
        ).all()
        return food_event
    
def get_patients(nutriologist_id: int):
    with DBManager() as db:
        patients = db.query(Users).filter(Users.nutriologist_id == nutriologist_id).all()
        return patients
    
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

class MenuPartRequest(BaseModel):
    food_event_id:int
    group_name: str
    description: str
    aliment: float
    amount: float
    unit: str

# Antes add_food_group
def add_menu_part(current_menu_part:MenuPartRequest):
    with DBManager() as db:
        new_menu_part = Menu_Part(
            food_event_id = current_menu_part.food_event_id,
            group_name = current_menu_part.group_name,
            description = current_menu_part.description,
            aliment = current_menu_part.aliment,
            amount = current_menu_part.amount,
            unit= current_menu_part.unit
        )
        db.add(new_menu_part)
        db.commit()
        print("Database food group: ",new_menu_part)
        return new_menu_part

def get_all_menu_parts_from_a_food_event(food_event_id: int):
    with DBManager() as db:
        menu_parts = db.query(Menu_Part).filter(Menu_Part.food_event_id == food_event_id).all()
        return menu_parts
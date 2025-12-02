from models.connection import DBManager
from models.models_db import User, FoodEvent, MenuPart
from pydantic import BaseModel

def get_all_food_by_id_nutriologist(nutriologist_id: int, patient_id: int):
    with DBManager() as db:
        food_event = db.query(FoodEvent).filter(
            (FoodEvent.nutriologist_id == nutriologist_id) & (FoodEvent.patient_id == patient_id)
        ).all()
        return food_event
    
def get_patients(nutriologist_id: int):
    with DBManager() as db:
        patients = db.query(User).filter(User.nutriologist_id == nutriologist_id).all()

        result = []
        for p in patients:
            patient_dict = {
                "id": p.id,
                "name": p.name,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "mail": p.mail,
                "age": p.age,
                "height": p.height,
                "goal_weight": p.goal_weight,
                "actual_weight": p.actual_weight,
                "gender": p.gender,
                "cellphone": p.cellphone,
                "last_visit": p.last_visit
            }
            result.append(patient_dict)

        return result



def add_patient(patient_id: int, nutri_id: int):
    with DBManager() as db:
        # Buscar al paciente por su ID
        patient = db.query(User).filter(User.id == patient_id).first()

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
        new_menu_part = MenuPart(
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
        menu_parts = db.query(MenuPart).filter(MenuPart.food_event_id == food_event_id).all()
        return menu_parts

class FoodEventRequest(BaseModel):
    food_name: str
    description:str | None
    patient_id: int

def add_food_event (current_food_event:FoodEventRequest, nutriologist_id:int):
    with DBManager() as db:
        new_food_event = FoodEvent(
            food_name = current_food_event.food_name,
            description = current_food_event.description,
            nutriologist_id = nutriologist_id,
            patient_id = current_food_event.patient_id
        )
        db.add(new_food_event)
        db.commit()
        return {
            'food_name':new_food_event.food_name, 
            'description':new_food_event.description,
            'patient_id':new_food_event.patient_id,
        }
    

from models.connection import DBManager
from models.models_db import Foods

def get_food_by_id_patient(patient_id: int):
    with DBManager() as db:
        food_event = db.query(Food_Event).filter(Food_Event.patient_id == patient_id).all()
        return food_event
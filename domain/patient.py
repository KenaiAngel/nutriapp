from models.connection import DBManager
from models.models_db import FoodEvent

def get_food_by_id_patient(patient_id: int):
    with DBManager() as db:
        food_event = db.query(FoodEvent).filter(FoodEvent.patient_id == patient_id).all()
        return food_event
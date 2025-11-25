from models.connection import DBManager
from models.models_db import Foods

def get_food_by_id_patient(patient_id: int):
    with DBManager() as db:
        foods = db.query(Foods).filter(Foods.patient_id == patient_id).all()
        return foods
from models.connection import DBManager
from models.models_db import FoodGroup, Aliment

def get_all_food_groups ():
    with DBManager as db:
        food_groups = db.query(FoodGroup).all()
        return food_groups
    
def get_all_aliments_by_food_group_id (group_id:int):
    with DBManager as db:
        aliments = db.query(Aliment).filter(Aliment.group_id == group_id).all()
        return aliments
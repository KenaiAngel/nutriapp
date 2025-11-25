from models.database import SessionLocal
from models.models_db import Users
#from domain.models import Foods
#from domain.models import Food_Groups

db = SessionLocal()
try:
    query = db.query(Users).all()
    for user in query:
        # Replace 'username' and 'email' with the actual attribute names of your class
        print(f"Username: {user.name}, Email: {user.mail} Role: {user.role}, id: {user.id}, id_nutri: {user.nutriologist_id}, pass: {user.hashed_password}")

    #query = db.query(Foods).all()
    #for food in query:
        # Replace 'username' and 'email' with the actual attribute names of your class
    #   print(f"ID: {food.id}, Name: {food.food_name} Description: {food.description}, Nuriolodoid: {food.nutriologist_id}, PatientId: {food.patient_id}")
    #query = db.query(Food_Groups).all()
    #for group in query:
        # Replace 'username' and 'email' with the actual attribute names of your class
    #   print(f"ID: {group.id}, Name: {group.group_name} Description: {group.description}, kcl: {group.kcal}, Protein: {group.protein}, Carbo: {group.carbohydrates}, fats: {group.fats}, Food_id:{group.food_id}")



finally:
    db.close()
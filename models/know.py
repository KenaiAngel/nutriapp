from models.database import SessionLocal
from models.models_db import Food_group, Aliment

db = SessionLocal()

try:

    print("\n--- LISTA DE ALIMENTOS ---")
    query_alimentos = db.query(Aliment).all()
    
    for food in query_alimentos:
        nombre_grupo = food.food_group.group_name if food.food_group else "Sin Grupo"
        
        print(f"ID: {food.id}, Alimento: {food.aliment_name}, "
              f"Cantidad: {food.amount} {food.unit}, "
              f"Grupo: {nombre_grupo}")

    print("\n" + "="*40 + "\n")
    print("--- GRUPOS DE ALIMENTOS ---")
    
    query_groups = db.query(Food_group).all()
    
    for group in query_groups:
        cantidad_alimentos = len(group.aliments)
        
        print(f"ID: {group.id}, Grupo: {group.group_name}, "
              f"Contiene: {cantidad_alimentos} alimentos")

finally:
    db.close()
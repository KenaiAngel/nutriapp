from models.database import SessionLocal
from models.models_db import FoodGroup, Aliment
from sqlalchemy.orm import joinedload
from sqlalchemy import func

# Inicialización de la sesión de base de datos
db = SessionLocal()

def know_data():
    try:

        print("\n## 1. Conteo General de Datos")
        total_groups = db.query(FoodGroup).count()
        total_aliments = db.query(Aliment).count()
        print(f"Número total de Grupos de Alimentos insertados: {total_groups}")
        print(f"Número total de Alimentos insertados: {total_aliments}")



        print("\n## 2. Grupos y su Contenido")
        group_counts = (
            db.query(FoodGroup.group_name, func.count(Aliment.id).label('num_aliments'))
            .outerjoin(Aliment)
            .group_by(FoodGroup.group_name)
            .order_by(FoodGroup.group_name)
            .all()
        )
        for group_name, count in group_counts:
            print(f"- {group_name}: {count} alimentos")
            


        print("\n## 3. Consultar un Grupo Específico (Frutas)")
        frutas_group = db.query(FoodGroup).filter(FoodGroup.group_name == "Frutas").options(joinedload(FoodGroup.aliments)).first()
        
        if frutas_group:
            print(f"Se encontraron {len(frutas_group.aliments)} alimentos en el grupo '{frutas_group.group_name}':")
            for aliment in frutas_group.aliments[:5]: # Mostrar solo los primeros 5
                print(f"  - {aliment.aliment_name} | Cantidad: {aliment.amount} {aliment.unit}")
        else:
            print("El grupo 'Frutas' no fue encontrado.")



        print('\n## 4. Alimentos medidos en "Rebanada"')
        rebanada_aliments = db.query(Aliment).filter(Aliment.unit == "Rebanada").all()
        
        if rebanada_aliments:
            print(f"Se encontraron {len(rebanada_aliments)} alimentos en rebanada:")
            for aliment in rebanada_aliments:
                print(f"  - {aliment.aliment_name} ({aliment.food_group.group_name}) | Eq: {aliment.amount} {aliment.unit}")
        else:
            print("No se encontraron alimentos medidos en 'Rebanada'.")

        print('\n## 5. Listado completo de Alimentos')
        all_aliments = db.query(Aliment).order_by(Aliment.aliment_name).all()
        
        if all_aliments:
            print(f"Listando los {len(all_aliments)} alimentos registrados:")
            for aliment in all_aliments:
                grupo = aliment.food_group.group_name if aliment.food_group else "---"
                
                print(f" | {aliment.aliment_name:30} | {grupo:20} | {aliment.amount} {aliment.unit}")
        else:
            print("La base de datos de alimentos está vacía.")

    except Exception as e:
        print(f"Error al intentar consultar la base de datos: {e}")
    finally:
        db.close()
        print("\n--- Consultas finalizadas. Conexión cerrada. ---")

if __name__ == "__main__":
    know_data()
from models.database import SessionLocal
from models.models_db import FoodGroup, Aliment

db = SessionLocal()

## Alimentos de medicion que se ocupan
## Taza
## Pieza
## g
## Rebanada
## Cucharada


data_equivalentes = {

    "Verduras": [
        ("Acelga", 0.5, "Taza"),
        ("Apio", 0.75, "Taza"),
        ("Berenjena", 0.75, "Taza"),
        ("Berro", 1.0, "Taza"),
        ("Betabel", 0.25, "Taza"),
        ("Brócoli", 0.5, "Taza"),
        ("Calabacita", 0.5, "Taza"),
        ("Champiñón", 0.5, "Taza"),
        ("Chayote", 0.5, "Taza"),
        ("Col", 0.5, "Taza"),
        ("Coliflor", 0.75, "Taza"),
        ("Ejotes", 0.5, "Taza"),
        ("Espárragos", 6.0, "Pieza"),
        ("Espinaca", 0.5, "Taza"),
        ("Flor de calabaza", 1.0, "Taza"),
        ("Germen de alfalfa", 2.0, "Taza"),
        ("Germen de soya", 0.33, "Taza"),
        ("Jícama", 0.5, "Taza"),
        ("Jitomate", 1.0, "Pieza"),
        ("Lechuga", 1.0, "Taza"),
        ("Nopal", 1.0, "Taza"),
        ("Pepino", 1.0, "Taza"),
        ("Rábano", 0.25, "Taza"),
        ("Salsa", 0.33, "Taza"),
        ("Setas", 0.5, "Taza"),
        ("Tomate", 5.0, "Pieza"),
        ("Verdolaga", 1.0, "Taza"),
        ("Zanahoria", 0.5, "Taza")
    ],
    "Frutas": [
        ("Arándano", 0.5, "Taza"),
        ("Capulín", 0.5, "Taza"),
        ("Cereza", 10.0, "Pieza"),
        ("Chabacano", 2.0, "Pieza"),
        ("Ciruela", 2.0, "Pieza"),
        ("Durazno", 2.0, "Pieza"),
        ("Frambuesa", 0.5, "Taza"),
        ("Guanábana", 0.25, "Pieza"),
        ("Guayaba", 2.0, "Pieza"),
        ("Higo", 2.0, "Pieza"),
        ("Kiwi", 1.0, "Pieza"),
        ("Limón", 4.0, "Pieza"),
        ("Mamey", 0.33, "Pieza"),
        ("Mandarina", 1.0, "Pieza"),
        ("Mango", 0.5, "Pieza"),
        ("Manzana", 1.0, "Pieza"),
        ("Melón", 1.0, "Taza"),
        ("Naranja", 1.0, "Pieza"),
        ("Nectarina", 1.0, "Pieza"),
        ("Papaya", 1.0, "Taza"),
        ("Pasas", 10.0, "Pieza"),
        ("Pera", 0.5, "Pieza"),
        ("Piña", 1.0, "Rebanada"),
        ("Plátano", 0.5, "Pieza"),
        ("Sandía", 1.0, "Taza"),
        ("Tamarindo", 0.25, "Taza"),
        ("Toronja", 0.5, "Pieza"),
        ("Tuna", 2.0, "Pieza")
    ],
    "Cereales y Tubérculos": [
        ("Amaranto", 0.25, "Taza"),
        ("Arroz blanco", 0.25, "Taza"),
        ("Arroz integral", 0.33, "Taza"),
        ("Avena en hojuelas", 2.0, "Cucharada"),
        ("Baguette", 0.14, "Pieza"),
        ("Barrita de avena", 0.5, "Pieza"),
        ("Bolillo", 0.33, "Pieza"),
        ("Cebada", 0.33, "Taza"),
        ("Cereal bajo en azúcar", 0.33, "Taza"),
        ("Crepas", 2.0, "Pieza"),
        ("Croutones", 0.5, "Taza"),
        ("Elote", 1.0, "Pieza"),
        ("Elote desgranado", 0.5, "Taza"),
        ("Pasta cocida", 0.33, "Taza"),
        ("Galletas bajas en azúcar", 2.0, "Pieza"),
        ("Galleta Habanera", 3.0, "Pieza"),
        ("Hot Cake", 1.0, "Pieza"),
        ("Palomitas de maíz sin sal", 2.5, "Taza"),
        ("Pan blanco", 1.0, "Rebanada"),
        ("Pan integral", 1.0, "Rebanada"),
        ("Pan tostado", 1.0, "Rebanada"),
        ("Papa cocida", 0.5, "Pieza"),
        ("Salvado de trigo", 2.0, "Cucharada"),
        ("Tortilla de maíz", 1.0, "Pieza"),
        ("Tortilla de harina", 0.5, "Pieza")
    ],
    "Leguminosas": [
        ("Alverjón", 0.5, "Taza"),
        ("Chícharo", 0.5, "Taza"),
        ("Garbanzo", 0.5, "Taza"),
        ("Frijol", 0.5, "Taza"),
        ("Haba", 0.5, "Taza"),
        ("Lenteja", 0.5, "Taza"),
        ("Soya cocida", 0.33, "Taza")
    ],
    "Alimentos de Origen Animal": [
        ("Carne de res", 60.0, "g"),
        ("Carne molida de res", 60.0, "g"),
        ("Carne de cerdo", 60.0, "g"),
        ("Carne molida de cerdo", 60.0, "g"),
        ("Carne de pollo", 50.0, "g"),
        ("Pierna o muslo de pollo", 1.0, "Pieza"),
        ("Jamón de pavo bajo en sodio", 2.0, "Rebanada"),
        ("Pechuga de pavo", 1.5, "Rebanada"),
        ("Pechuga de pollo aplanada", 40.0, "g"),
        ("Atún en agua", 0.5, "Lata"),
        ("Camarón", 5.0, "Pieza"),
        ("Charales", 1.0, "Cucharada"),
        ("Filete de mojarra", 50.0, "g"),
        ("Filete de pescado", 40.0, "g"),
        ("Jaiba", 0.33, "Taza"),
        ("Salmón", 50.0, "g"),
        ("Clara de huevo", 2.0, "Pieza"),
        ("Huevo cocido", 1.0, "Pieza"),
        ("Huevo revuelto", 1.0, "Pieza"),
        ("Huevo frito", 1.0, "Pieza"),
        ("Queso panela", 40.0, "g"),
        ("Queso cottage", 3.0, "Cucharada"),
        ("Queso Oaxaca", 30.0, "g")
    ],
    "Leche": [
        ("Leche", 1.0, "Taza"),
        ("Leche de soya", 1.0, "Taza"),
        ("Yogurt natural sin azúcar", 2.0, "Cucharada")
    ],
    "Aceites y Grasas sin proteína": [
        ("Aceite de canola", 1.0, "Cucharadita"),
        ("Aceite de oliva", 1.0, "Cucharadita"),
        ("Aceite de uva", 1.0, "Cucharadita"),
        ("Aceite de aguacate", 1.0, "Cucharadita"),
        ("Aceite en spray", 5.0, "Segundo"),
        ("Aceitunas", 5.0, "Pieza"),
        ("Aderezo italiano", 0.5, "Cucharada"),
        ("Aderezo de mostaza", 0.5, "Cucharada"),
        ("Aderezo vinagreta", 0.5, "Cucharada"),
        ("Aguacate", 0.33, "Pieza"),
        ("Crema baja en grasa", 1.0, "Cucharada"),
        ("Margarina baja en sal", 1.0, "Cucharadita"),
        ("Mayonesa baja en grasa", 1.0, "Cucharadita"),
        ("Queso crema bajo en grasa", 1.0, "Cucharada")
    ],
    "Oleaginosas": [
        ("Ajonjolí", 4.0, "Cucharadita"),
        ("Almendra", 10.0, "Pieza"),
        ("Avellana", 9.0, "Pieza"),
        ("Cacahuate tostado sin sal", 14.0, "Pieza"),
        ("Chía", 1.0, "Cucharadita"),
        ("Nuez", 3.0, "Pieza"),
        ("Nuez de la India", 7.0, "Pieza"),
        ("Pepitas de calabaza", 1.0, "Cucharada"),
        ("Pepitas de melón", 1.0, "Cucharada"),
        ("Piñón", 1.0, "Cucharada"),
        ("Pistache sin sal", 10.0, "Pieza")
    ]
}

def seed_data():
    try:
        print("Iniciando la inserción de datos...")
        
        for group_name, foods_list in data_equivalentes.items():
            
            # 1. Crear o buscar el Grupo (FoodGroup)
            existing_group = db.query(FoodGroup).filter(FoodGroup.group_name == group_name).first()
            
            if not existing_group:
                new_group = FoodGroup(group_name=group_name)
                db.add(new_group)
                db.flush() 
                group_id = new_group.id
                print(f"Creado nuevo grupo: {group_name}")
            else:
                group_id = existing_group.id
                print(f"Grupo existente encontrado: {group_name}")

            # 2. Insertar los Alimentos (Aliment)
            count = 0
            for name, amount, unit in foods_list:
                
                # Verificamos si ya existe para evitar duplicados
                existing_aliment = db.query(Aliment).filter(
                    Aliment.aliment_name == name, 
                    Aliment.group_id == group_id
                ).first()

                if not existing_aliment:
                    new_aliment = Aliment(
                        aliment_name=name,
                        amount=amount, # Ya es float
                        unit=unit,     # Ya es string limpio
                        group_id=group_id
                    )
                    db.add(new_aliment)
                    count += 1
            
            print(f"  -> Insertados {count} alimentos nuevos en {group_name}")

        db.commit()
        print("\n¡Datos insertados exitosamente!")

    except Exception as e:
        db.rollback()
        print(f"Error crítico durante la inserción: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
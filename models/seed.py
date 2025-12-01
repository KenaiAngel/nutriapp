from models.database import SessionLocal
from models.models_db import Food_Groups, Aliment 

db = SessionLocal()

def parse_quantity(quantity_str):

    parts = quantity_str.split(' ', 1) 
    val_str = parts[0]
    unit = parts[1] if len(parts) > 1 else "Pieza" 
    
    amount = 0.0
    
    try:
        if '/' in val_str:
            num, den = val_str.split('/')
            amount = float(num) / float(den)
        else:
            amount = float(val_str)
    except ValueError:
        amount = 1.0 
        
    return amount, unit

data_equivalentes = {
    "Verduras": [
        ("Acelga", "1/2 Taza"), ("Apio", "3/4 Taza"), ("Berenjena", "3/4 Taza"),
        ("Berro", "1 Taza"), ("Betabel", "1/4 Taza"), ("Brócoli", "1/2 Taza"),
        ("Calabacita", "1/2 Taza"), ("Champiñón", "1/2 Taza"), ("Chayote", "1/2 Taza"),
        ("Col", "1/2 Taza"), ("Coliflor", "3/4 Taza"), ("Ejotes", "1/2 Taza"),
        ("Espárragos", "6 Piezas"), ("Espinaca", "1/2 Taza"), ("Flor de calabaza", "1 Taza"),
        ("Germen de alfalfa", "2 Tazas"), ("Jícama", "1/2 Taza"), ("Jitomate", "1 Pieza"),
        ("Lechuga", "1 Taza"), ("Nopal", "1 Taza"), ("Pepino", "1 Taza"),
        ("Rábano", "1/4 Taza"), ("Salsa", "1/3 Taza"), ("Setas", "1/2 Taza"),
        ("Tomate", "5 Piezas"), ("Verdolaga", "1 Taza"), ("Zanahoria", "1/2 Taza")
    ],
    "Frutas": [
        ("Arándano", "1/2 Taza"), ("Capulín", "1/2 Taza"), ("Cereza", "10 Piezas"),
        ("Chabacano", "2 Piezas"), ("Ciruela", "2 Piezas"), ("Durazno", "2 Piezas"),
        ("Frambuesa", "1/2 Taza"), ("Guanábana", "1/4 Pieza"), ("Guayaba", "2 Piezas"),
        ("Higo", "2 Piezas"), ("Kiwi", "1 Pieza"), ("Limón", "4 Piezas"),
        ("Mamey", "1/3 Pieza"), ("Mandarina", "1 Pieza"), ("Mango", "1/2 Pieza"),
        ("Manzana", "1 Pieza"), ("Melón", "1 Taza"), ("Naranja", "1 Pieza"),
        ("Nectarina", "1 Pieza"), ("Papaya", "1 Taza"), ("Pasas", "10 Piezas"),
        ("Pera", "1/2 Pieza"), ("Piña", "1 Rebanada"), ("Plátano", "1/2 Pieza"),
        ("Sandía", "1 Taza"), ("Tamarindo", "1/4 Taza"), ("Toronja", "1/2 Pieza"),
        ("Tuna", "2 Piezas")
    ],
    "Cereales y Tubérculos": [
        ("Amaranto", "1/4 Taza"), ("Arroz blanco", "1/4 Taza"), ("Arroz integral", "1/3 Taza"),
        ("Avena en hojuelas", "2 Cucharadas"), ("Baguette", "1/7 Pieza"), ("Barrita de avena", "1/2 Pieza"),
        ("Bolillo", "1/3 Pieza"), ("Cebada", "1/3 Taza"), ("Cereal bajo en azúcar", "1/3 Taza"),
        ("Crepas", "2 Piezas"), ("Croutones", "1/2 Taza"), ("Elote", "1 Pieza"),
        ("Elote desgranado", "1/2 Taza"), ("Pasta cocida", "1/3 Taza"), ("Galletas bajas en azúcar", "2 Piezas"),
        ("Galleta Habanera", "3 Piezas"), ("Hot Cake", "1 Pieza"), ("Palomitas naturales", "2.5 Tazas"),
        ("Pan blanco", "1 Rebanada"), ("Pan integral", "1 Rebanada"), ("Pan tostado", "1 Rebanada"),
        ("Papa cocida", "1/2 Pieza"), ("Salvado de trigo", "2 Cucharadas"), ("Tortilla de maíz", "1 Pieza"),
        ("Tortilla de harina", "1/2 Pieza")
    ],
    "Leguminosas": [
        ("Alverjón", "1/2 Taza"), ("Chícharo", "1/2 Taza"), ("Garbanzo", "1/2 Taza"),
        ("Frijol", "1/2 Taza"), ("Haba", "1/2 Taza"), ("Lenteja", "1/2 Taza"),
        ("Soya cocida", "1/3 Taza")
    ],
    "Alimentos de Origen Animal": [
        ("Carne de res", "60 g"), ("Carne molida de res", "60 g"), ("Carne de cerdo", "60 g"),
        ("Carne de pollo", "50 g"), ("Pechuga de pavo", "1.5 Rebanadas"), ("Atún en agua", "50 g"),
        ("Camarón", "5 Piezas"), ("Filete de pescado", "40 g"), ("Salmón", "50 g"),
        ("Clara de huevo", "2 Piezas"), ("Huevo cocido", "1 Pieza"), ("Queso panela", "40 g"),
        ("Queso Oaxaca", "30 g"), ("Queso cottage", "3 Cucharadas")
    ],
    "Leche": [
        ("Leche", "1 Taza"), ("Leche de soya", "1 Taza"), ("Yogurt natural", "2 Cucharadas")
    ],
    "Aceites y Grasas": [
        ("Aceite de canola", "1 Cucharadita"), ("Aceite de oliva", "1 Cucharadita"),
        ("Aguacate", "1/3 Pieza"), ("Aceitunas", "5 Piezas"), ("Crema baja en grasa", "1 Cucharada"),
        ("Mayonesa", "1 Cucharadita"), ("Queso crema", "1 Cucharada")
    ],
    "Oleaginosas": [
        ("Ajonjolí", "4 Cucharaditas"), ("Almendra", "10 Piezas"), ("Avellana", "9 Piezas"),
        ("Cacahuate", "14 Piezas"), ("Chía", "1 Cucharadita"), ("Nuez", "3 Piezas"),
        ("Pistache", "10 Piezas")
    ]
}

def seed_data():
    try:
        print("Iniciando carga de alimentos...")
        
        for group_name, alimentos_list in data_equivalentes.items():
            # 1. Crear el Grupo de Alimento
            # Asumiendo que Food_Groups tiene campos: group_name (y tal vez descripción)
            # Nota: El seed original tenía macros en el grupo, pero las imagenes
            # muestran listas simples. Ajustaré a solo crear el nombre del grupo.
            new_group = Food_Groups(
                group_name=group_name,
                description=f"Lista de equivalentes para {group_name}"
                # Si tu modelo requiere macros obligatorios, añade valores dummy o 0.0 aquí
            )
            
            db.add(new_group)
            db.flush() # Hacemos flush para obtener el ID del grupo recién creado (new_group.id)
            
            # 2. Insertar los alimentos de ese grupo
            for nombre_alimento, cantidad_str in alimentos_list:
                amount, unit = parse_quantity(cantidad_str)
                
                new_aliment = Aliment(
                    group_id=new_group.id,  # Llave foránea al grupo
                    aliment_name=nombre_alimento,
                    amount=amount,
                    unit=unit
                )
                db.add(new_aliment)
            
            print(f"Grupo '{group_name}' cargado con {len(alimentos_list)} alimentos.")

        db.commit()
        print("¡Base de datos poblada exitosamente!")

    except Exception as e:
        db.rollback()
        print(f"Algo salió mal: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

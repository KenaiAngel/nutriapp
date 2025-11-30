from models.database import SessionLocal
from models.models_db import Users, Foods, Food_Groups
from security.encrypt import hash_password

db = SessionLocal()

try:
    hash = hash_password('123')
    nutri =  Users(
        name= 'Yuquin', 
        first_name = 'Quin',
        last_name = 'Quin',
        mail = 'nutri@gmail.com',
        hashed_password= hash,
        role = 'NUTRIOLOGO'
    )
    patien =  Users(
        name= 'Yuquin', 
        first_name = 'Quin',
        last_name = 'Quin',
        mail = 'pa@gmail.com',
        hashed_password= hash,
        role = 'PACIENTE'
    )


    db.add(nutri)
    db.add(patien)
    db.commit()
    
    desayuno = Foods(
        food_name = 'Desayuno',
        description = 'Aqui desayunas',
        nutriologist_id = 2,
        patient_id = 3
    )

    pan = Food_Groups(
        group_name = 'Proteinas',
        description = 'Aqui se come',
        kcal =  12.2,
        protein = 12.2,
        carbohydrates = 12.2, 
        fats = 12.2,
        food_id = 1
    )

    db.add(desayuno)
    db.add(pan)
    db.commit()

except:
    print('Algo salio mal')

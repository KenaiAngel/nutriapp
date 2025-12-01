from models.connection import DBManager
from models.models_db import FoodEvent, FoodEventRegister, MenuRegister
from pydantic import BaseModel
from datetime import date
from sqlalchemy import and_

def get_food_by_id_patient(patient_id: int):
    with DBManager() as db:
        food_event = db.query(FoodEvent).filter(FoodEvent.patient_id == patient_id).all()
        return food_event


class MenuRegisterRequest(BaseModel): 
    date: date
    food_event_id: int

    group_name: str
    description: str | None
    aliment: str
    amount: float
    unit: str


def add_new_register(current_register: MenuRegisterRequest):
    with DBManager() as db:
        # Revisar si el MenuRegister ya existe
        exist_register = db.query(MenuRegister).filter(
            and_(
                MenuRegister.group_name == current_register.group_name,
                MenuRegister.aliment == current_register.aliment,
                MenuRegister.amount == current_register.amount,
                MenuRegister.unit == current_register.unit,
                MenuRegister.food_event_id == current_register.food_event_id
            )
        ).first()

        if not exist_register:
            # Crear nuevo MenuRegister si no existe
            exist_register = MenuRegister(
                group_name=current_register.group_name,
                aliment=current_register.aliment,
                amount=current_register.amount,
                unit=current_register.unit,
                food_event_id=current_register.food_event_id
            )
            db.add(exist_register)
            db.commit()
            db.refresh(exist_register)  # Para obtener el id generado

        # Crear nuevo FoodEventRegister para marcar la fecha
        new_food_event_register = FoodEventRegister(
            date=current_register.date,
            food_event_id=current_register.food_event_id,
            menu_register_id=exist_register.id
        )
        db.add(new_food_event_register)
        db.commit()
        db.refresh(new_food_event_register)

        result = {
            'date': new_food_event_register.date,
            'group_name': exist_register.group_name,
            'aliment': exist_register.aliment,
            'amount': exist_register.amount,
            'unit': exist_register.unit
        }

        return result



def get_all_registers_date_food_id(date:date, food_event_id:int):
    with DBManager() as db:
        # Obtener todos los registros del evento y fecha indicados
        event_registers = db.query(FoodEventRegister).filter(
            and_(
                FoodEventRegister.date == date,
                FoodEventRegister.food_event_id == food_event_id
            )
        ).all()

        if not event_registers:
            return []

        # Lista para almacenar los MenuRegister asociados
        menu_registers_list = []

        for register in event_registers:
            # Por cada registro, obtenemos el MenuRegister relacionado
            menu_register = db.query(MenuRegister).filter(
                MenuRegister.id == register.menu_register_id
            ).first()

            if menu_register:

                menu_registers_list.append({
                    "id": menu_register.id,
                    "group_name": menu_register.group_name,
                    "description": menu_register.description,
                    "aliment": menu_register.aliment,
                    "amount": menu_register.amount,
                    "unit": menu_register.unit
                })

        return menu_registers_list
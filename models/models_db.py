from datetime import date
from models.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    age = Column(Integer)
    height = Column(Float)
    goal_weight = Column(Float)
    actual_weight = Column(Float)
    gender = Column(String)
    cellphone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    last_visit = Column(Date)

    mail = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="PACIENTE")
    nutriologist_id = Column(Integer, default=None)

    # Relaciones
    foods_as_nutriologist = relationship(
        "FoodEvent",
        foreign_keys="FoodEvent.nutriologist_id",
        back_populates="nutriologist"
    )

    foods_as_patient = relationship(
        "FoodEvent",
        foreign_keys="FoodEvent.patient_id",
        back_populates="patient"
    )
class FoodEvent(Base):
    __tablename__ = 'food_event'

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)
    description = Column(String)

    nutriologist_id = Column(Integer, ForeignKey('users.id'))
    patient_id = Column(Integer, ForeignKey('users.id'))

    nutriologist = relationship(
        "User",
        foreign_keys=[nutriologist_id],
        back_populates="foods_as_nutriologist"
    )

    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="foods_as_patient"
    )

    # Relación: un FoodEvent tiene muchos MenuRegister base
    menu_items = relationship(
        "MenuRegister",
        back_populates="food_event"
    )

    menu_parts = relationship(
        "MenuPart", 
        back_populates="food_event"
    )

    # Relación: registros por fecha
    daily_logs = relationship(
        "FoodEventRegister",
        back_populates="food_event"
    )

class MenuPart(Base):
    __tablename__ = 'menu_part'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    description = Column(String)
    aliment = Column(String)
    amount = Column(Float)
    unit = Column(String)

    food_event_id = Column(Integer, ForeignKey('food_event.id'))

    food_event = relationship(
        "FoodEvent", 
        back_populates="menu_parts"
    )


class FoodEventRegister(Base):
    __tablename__ = 'food_event_register'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    food_event_id = Column(Integer, ForeignKey('food_event.id'), nullable=False)
    menu_register_id = Column(Integer, ForeignKey('menu_register.id'), nullable=False)

    # Relación hacia el evento principal
    food_event = relationship(
        "FoodEvent",
        back_populates="daily_logs"
    )

    # Relación hacia un alimento del menú base
    menu_register = relationship(
        "MenuRegister",
        back_populates="daily_usages"
    )


class MenuRegister(Base):
    __tablename__ = 'menu_register'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    description = Column(String)
    aliment = Column(String)
    amount = Column(Float)
    unit = Column(String)

    # Relación hacia FoodEvent (menú base)
    food_event_id = Column(Integer, ForeignKey("food_event.id"))
    food_event = relationship("FoodEvent", back_populates="menu_items")

    # Relación hacia fechas donde este alimento fue usado
    daily_usages = relationship(
        "FoodEventRegister",
        back_populates="menu_register"
    )


class Aliment(Base):
    __tablename__ = 'aliment'

    id = Column(Integer, primary_key=True, index=True)
    aliment_name = Column(String)
    amount = Column(Float)
    unit = Column(String)

    group_id = Column(Integer, ForeignKey('food_group.id'))

    food_group = relationship("FoodGroup", back_populates="aliments")

class FoodGroup(Base):
    __tablename__ = 'food_group'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)

    aliments = relationship("Aliment", back_populates="food_group")

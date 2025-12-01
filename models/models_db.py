from sqlite3 import Date
from models.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    age = Column(int)                       
    height = Column(float)                  
    goal_weight = Column(float)             
    actual_weight = Column(float)           
    gender = Column(String)                 
    cellphone = Column(String)              
    first_name = Column(String)             
    last_name = Column(String)              
    last_visit = Column(Date)           
    
    mail = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="PACIENTE")
    nutriologist_id = Column(Integer, default=None)

    # 🔹 Relaciones bidireccionales
    foods_as_nutriologist = relationship(
        "Foods",
        foreign_keys="Foods.nutriologist_id",
        back_populates="nutriologist"
    )
    foods_as_patient = relationship(
        "Foods",
        foreign_keys="Foods.patient_id",
        back_populates="patient"
    )

class Food_Event(Base):
    __tablename__ = 'Food_Event'

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)
    description = Column(String)

    # 🔹 Llaves foráneas
    nutriologist_id = Column(Integer, ForeignKey('users.id'))
    patient_id = Column(Integer, ForeignKey('users.id'))

    # 🔹 Relaciones con Users
    nutriologist = relationship(
        "Users",
        foreign_keys=[nutriologist_id],
        back_populates="foods_as_nutriologist"
    )
    patient = relationship(
        "Users",
        foreign_keys=[patient_id],
        back_populates="foods_as_patient"
    )

    # 🔹 Relación con Food_Groups
    groups = relationship(
        "Menu_part",
        back_populates="food"
    )


class Menu_part(Base):
    __tablename__ = 'Menu_part'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    description = Column(String)
    equivalent = Column(Float)
    aliment = Column(String)
    amount = Column(Float)
    unit = Column(String)

    # Llave foránea hacia Foods
    food_event_id = Column(Integer, ForeignKey('Food_Events.id'))

    # Relación inversa
    food = relationship(
        "Food_Event",
        back_populates="groups"
    )

class Part_register(Base):
    __tablename__ = 'Part_register'

    date = Column(Date)

    id_part = Column(Intenger, ForeignKey('Menu_part.id'))
    id_register = Column(Intenger, ForeignKey('Menu_register.id'))

    # Relación inversa a Menu_part
    part = relationship(
        "Menu_part",
        backref="Part_register"
    )

    # Relación inversa a Menu_register
    menu_register = relationship(
        "Menu_register",
        backref="Part_register"
    )

class Menu_register(Base):
    __tablename__ = 'Menu_register'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    description = Column(String)
    equivalent = Column(Float)
    aliment = Column(String)
    amount = Column(Float)
    unit = Column(String)

    parts = relationship(
        "Part_register",
        backref="Menu_register"
    )

class Aliment(Base):
    __tablename__ = 'Aliment'

    id = Column(Integer, primary_key=True, index=True)
    aliment_name = Column(String)
    amount = Column(Float)
    unit = Column(String)

    # Llave foránea hacia Food_group
    group_id = Column(Integer, ForeignKey('Food_group.id'))

    # Relación inversa a Food_group
    food_group = relationship(
        "Food_group",
        backref="Aliment"
    )

class Food_group(Base):
    __tablename__ = 'Food_group'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    # Relación inversa a Aliments
    aliments = relationship(
        "Aliment",
        backref="Food_group"
    )

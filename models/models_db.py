from models.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    mail = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
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

class Foods(Base):
    __tablename__ = 'foods'

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
        "Food_Groups",
        back_populates="food"
    )


class Food_Groups(Base):
    __tablename__ = 'food_groups'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    description = Column(String)
    kcal = Column(Float)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)

    # Llave foránea hacia Foods
    food_id = Column(Integer, ForeignKey('foods.id'))

    # Relación inversa
    food = relationship(
        "Foods",
        back_populates="groups"
    )

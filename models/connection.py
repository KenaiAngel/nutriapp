from typing import Annotated
from sqlalchemy.orm import Session
from models.database import SessionLocal

#import domain.models as models



class DBManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

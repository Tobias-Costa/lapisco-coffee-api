from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from src.database.db import Base

class CoffeeState(Base):
    __tablename__ = "coffee_state"

    id = Column(Integer, primary_key=True, index=True)
    peso_gramas = Column(Float, default=0.0)
    esta_fazendo = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

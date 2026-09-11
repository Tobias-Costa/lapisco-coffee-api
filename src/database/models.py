from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from src.database.db import Base

FUSO_LOCAL = ZoneInfo("America/Sao_Paulo")

def obter_horario():
    return datetime.now(FUSO_LOCAL)

class CoffeeState(Base):
    __tablename__ = "coffee_state"

    id = Column(Integer, primary_key=True, index=True)
    peso_gramas = Column(Float, default=0.0)
    esta_fazendo = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), default=obter_horario, onupdate=obter_horario)

from api.database.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Float

class CoffeeSensor(Base):
    __tablename__ = "CoffeeSensor"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    device_id = Column(String, nullable=False)
    level_value = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
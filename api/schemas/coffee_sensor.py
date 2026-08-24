from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CoffeeSensorBase(BaseModel):
    device_id: str
    level_value: float
    description: Optional[str] = None

    class Config:
        orm_mode = True

class CoffeeSensorResponse(CoffeeSensorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CoffeeSensorCreate(CoffeeSensorBase):
    class Config:
        orm_mode = True
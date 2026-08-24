from typing import List
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.database import models
from api.database.db import get_db
from api.schemas.coffee_sensor import CoffeeSensorResponse, CoffeeSensorCreate
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/coffee/sensor",
    tags=["Coffee Sensor"]
)

@router.get("/", response_model=List[CoffeeSensorResponse])
def get_coffee_level(db: Session = Depends(get_db)):
    coffee_query = db.query(models.CoffeeSensor).all()
    return coffee_query


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[CoffeeSensorCreate])
def create_coffee_log(coffe_sensor_create: CoffeeSensorCreate, db: Session = Depends(get_db)):
    new_log = models.CoffeeSensor(**coffe_sensor_create.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return [new_log]
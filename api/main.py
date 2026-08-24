from fastapi import FastAPI
from api.database.db import engine, Base
from api.routers import coffee_sensor
import psycopg2

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(coffee_sensor.router)

@app.get("/")
async def root():
    return {"API working": "Success!"}

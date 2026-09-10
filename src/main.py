from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.db import engine, Base
from src.routers import coffee_sensor

app = FastAPI(title="Lapiscoffee")

# Ativa o CORS para liberar o acesso de qualquer origem/porta (ex: Postman, React, HTML local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permite requisições de qualquer endereço 
    allow_credentials=True,
    allow_methods=["*"],        # Permite todos os métodos (GET, POST, etc)
)

# Cria as tabelas no banco de dados na inicialização
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(coffee_sensor.router)

@app.get("/")
async def root():
    return {"API working": "Success!"}

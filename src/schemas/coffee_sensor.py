from pydantic import BaseModel

# Validação para entrada de peso
class PesoInput(BaseModel):
    peso_gramas: float

# Validação para entrada de status de preparo
class StatusInput(BaseModel):
    esta_fazendo: bool

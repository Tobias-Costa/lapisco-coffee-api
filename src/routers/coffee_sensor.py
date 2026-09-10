import asyncio
import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.db import get_db
from src.database.models import CoffeeState
from src.schemas.coffee_sensor import PesoInput, StatusInput

router = APIRouter(prefix="/api/coffee", tags=["Coffee Monitor"])

# Fila global para gerenciar as atualizações de forma sequencial
coffee_queue = asyncio.Queue()

# Busca o último estado ou inicializa se estiver vazio
async def obter_estado_atual(db: AsyncSession):
    result = await db.execute(select(CoffeeState).order_by(CoffeeState.id.desc()))
    estado = result.scalars().first()
    if not estado:
        estado = CoffeeState(peso_gramas=0.0, esta_fazendo=False)
        db.add(estado)
        await db.flush()
    return estado

# Formata os dados unificados e insere na fila de transmissão
async def empurrar_para_stream(estado):
    status_texto = "Fazendo" if estado.esta_fazendo else "Pronto"
    dados_unificados = {
        "peso_gramas": estado.peso_gramas,
        "status": status_texto,
        "timestamp": str(estado.timestamp)
    }
    # Adiciona o JSON na fila de transmissão
    await coffee_queue.put(dados_unificados)

@router.post("/peso", status_code=status.HTTP_200_OK)
async def atualizar_peso(payload: PesoInput, db: AsyncSession = Depends(get_db)):
    estado = await obter_estado_atual(db)
    estado.peso_gramas = payload.peso_gramas
    await db.flush()
    
    # Gera a atualização na hora
    await empurrar_para_stream(estado)
    return {"message": "Peso atualizado com sucesso"}

@router.post("/status", status_code=status.HTTP_200_OK)
async def atualizar_status(payload: StatusInput, db: AsyncSession = Depends(get_db)):
    estado = await obter_estado_atual(db)
    estado.esta_fazendo = payload.esta_fazendo
    await db.flush()
    await empurrar_para_stream(estado)
    return {"message": "Status de preparo atualizado"}

@router.get("/stream")
async def coffee_stream():
    async def sse_generator():
        while True:
            # Aguarda novos dados entrarem na fila
            dados = await coffee_queue.get()
            # Envia o pacote formatado como um evento de Server-Sent Events
            yield f"data: {json.dumps(dados)}\n\n"

    # Cabeçalhos HTTP para desativar cache e forçar streaming em tempo real
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "X-Accel-Buffering": "no"
    }

    return StreamingResponse(sse_generator(), headers=headers, media_type="text/event-stream")

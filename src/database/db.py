import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega variáveis do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Motor assíncrono do banco de dados
engine = create_async_engine(DATABASE_URL, echo=False)

# Gerador de sessões assíncronas
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Dependência para gerenciamento de sessão nas rotas
async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()

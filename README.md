# ☕ Lapiscoffee API: Smart Coffee Monitor - LAPISCO

Este projeto é uma API RESTful assíncrona de alta performance desenvolvida para o monitoramento em tempo real de cafeteiras inteligentes utilizando IoT. O sistema recebe dados independentes de sensores físicos (massa de café e status de operação) e transmite o estado unificado instantaneamente através de Server-Sent Events (SSE).

## 🛠️ Stacks Utilizadas

*   **Python** — Linguagem base com suporte nativo a concorrência assíncrona.
*   **FastAPI** — Framework web assíncrono moderno e focado em altíssima performance.
*   **SQLAlchemy & Asyncpg** — ORM e driver assíncrono especializado para PostgreSQL.
*   **Docker & Docker Compose** — Conteinerização e orquestração do ambiente isolado.
*   **PostgreSQL** — Sistema de gerenciamento de banco de dados relacional.

## 🚀 Como Configurar o Ambiente de Desenvolvimento (Docker)

Siga os passos abaixo para clonar, configurar e rodar o projeto em um ambiente totalmente conteinerizado.

### 1. Clonar o Repositório
```bash
git clone https://github.com/Tobias-Costa/lapisco-coffee-api.git
cd lapisco-coffee-api
```

### 2. Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na **raiz do projeto** e insira as configurações abaixo:

```env
# Database Settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[SUA-SENHA-AQUI]
POSTGRES_DB=coffee_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SQLAlchemy Connection String
DATABASE_URL=postgresql+asyncpg://postgres:[SUA-SENHA-AQUI]@db:5432/coffee_db
```

### 3. Buildar e Inicializar os Containers
Com o arquivo `.env` configurado, inicialize a aplicação e o banco de dados com o Docker Compose:

```bash
docker-compose up --build
```
*O Docker cuidará automaticamente de ler o arquivo `.env`, baixar as imagens necessárias, instalar as dependências do `requirements.txt`, aplicar o healthcheck de conectividade e expor o servidor.*

A API estará disponível no endereço local: `http://127.0.0.1:8000`.

Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`.

---

## 📁 Estrutura de Pastas do Projeto

```text
lapiscoffee/
├── .env                       # Arquivo com as credenciais ocultas do banco
├── docker-compose.yml         # Orquestração do Postgres e da API
├── Dockerfile                 # Instalação do Python e inicialização da aplicação
├── requirements.txt           # Dependências assíncronas do sistema
└── app/                       # Diretório principal da aplicação
    ├── __init__.py
    ├── main.py                # Ponto de entrada (CORS e inicialização)
    ├── database/              # Persistência e modelagem
    │   ├── __init__.py
    │   ├── db.py              # Conexão assíncrona (SQLAlchemy + asyncpg)
    │   └── models.py          # Tabela do banco de dados (coffee_state)
    ├── routers/               # Endpoints da aplicação
    ├── __init__.py
    │   └── coffee_sensor.py   # Lógica das rotas e Fila de Streaming
    └── schemas/               # Validação de dados (Pydantic v2)
    ├── __init__.py
        └── coffee_sensor.py   # Estrutura de PesoInput e StatusInput
```

---

## 🛣️ Endpoints da API

### Monitor da Cafeteira (`/api/coffee/`)

| Método | Endpoint | Descrição | Parâmetros da URL / Corpo |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/coffee/peso` | Atualiza a quantidade de massa de café na balança | JSON `{"peso_gramas": float}` |
| **POST** | `/api/coffee/status` | Informa se a cafeteira mudou seu estado lógico | JSON `{"esta_fazendo": bool}` |
| **GET** | `/api/coffee/stream` | Canal contínuo de logs unificados em tempo real (SSE) | Nenhum *(Retorna fluxo contínuo)* |

---

### 1. Atualizar Peso do Café
* **URL:** `/api/coffee/peso`
* **Método:** `POST`
* **Payload (JSON):**
```json
{
  "peso_gramas": 250.7
}
```

### 2. Atualizar Status de Preparo
* **URL:** `/api/coffee/status`
* **Método:** `POST`
* **Payload (JSON):**
```json
{
  "esta_fazendo": true
}
```
> *Nota: Use `true` para indicar que a cafeteira está **"Fazendo"** e `false` para indicar que o café está **"Pronto"**.*

### 3. Fluxo de Logs em Tempo Real (SSE)
* **URL:** `/api/coffee/stream`
* **Método:** `GET`
* **Content-Type:** `text/event-stream`
* **Exemplo de Retorno Contínuo:**

```json
{"peso_gramas": 250.7, "status": "Fazendo", "timestamp": "2026-09-10 03:30:15"}
```

---
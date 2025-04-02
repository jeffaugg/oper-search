from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

app = FastAPI(
    title="API de Operadoras de Saúde",
    description="API para consulta de operadoras de planos de saúde",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    # Aguardar o PostgreSQL ficar pronto
    await wait_for_db()
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    # Importar dados
    from .services.data_importer import import_data
    import_data()

async def wait_for_db():
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            if attempt == max_retries - 1:
                raise
            time.sleep(retry_delay)

# Importar rotas depois para evitar import circular
from .routes import operadoras
app.include_router(operadoras.router, prefix="/api/v1")

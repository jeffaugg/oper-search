import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
from ..models.operadora import Operadora
from datetime import datetime
import os

def import_data():
    db = next(get_db())
    try:
        # Verificar se já existem dados
        if db.query(Operadora).count() == 0:
            print("Importando dados do CSV...")
            import_from_csv(db)
            print("Dados importados com sucesso!")
        else:
            print("Dados já existem no banco, pulando importação.")
    finally:
        db.close()

def import_from_csv(db: Session):
    file_path = "/app/Index.csv"
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado em {file_path}")
    
    # Limpar tabela
    db.execute(text("TRUNCATE TABLE operadoras RESTART IDENTITY CASCADE"))
    
    chunksize = 500
    for chunk in pd.read_csv(
        file_path,
        sep=";",
        dtype=str,
        chunksize=chunksize,
        encoding='utf-8',
        na_filter=False
    ):
        chunk.columns = chunk.columns.str.strip()
        records = []
        
        for _, row in chunk.iterrows():
            record = Operadora(
                Registro_ANS=row.get('Registro_ANS'),
                CNPJ=row.get('CNPJ'),
                Razao_Social=row.get('Razao_Social'),
                Nome_Fantasia=row.get('Nome_Fantasia'),
                Modalidade=row.get('Modalidade'),
                Logradouro=row.get('Logradouro'),
                Numero=row.get('Numero'),
                Complemento=row.get('Complemento'),
                Bairro=row.get('Bairro'),
                Cidade=row.get('Cidade'),
                UF=row.get('UF'),
                CEP=row.get('CEP'),
                DDD=row.get('DDD'),
                Telefone=row.get('Telefone'),
                Fax=row.get('Fax'),
                Endereco_eletronico=row.get('Endereco_eletronico'),
                Representante=row.get('Representante'),
                Cargo_Representante=row.get('Cargo_Representante'),
                Regiao_de_Comercializacao=row.get('Regiao_de_Comercializacao'),
                Data_Registro_ANS=parse_date(row.get('Data_Registro_ANS'))
            )
            records.append(record)
        
        db.bulk_save_objects(records)
        db.commit()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except:
        return None
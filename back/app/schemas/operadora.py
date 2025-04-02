from datetime import date
from typing import Optional
from pydantic import BaseModel

class OperadoraBase(BaseModel):
    Registro_ANS: str
    CNPJ: str
    Razao_Social: str
    Nome_Fantasia: Optional[str] = None
    Modalidade: str
    Logradouro: str
    Numero: Optional[str] = None
    Complemento: Optional[str] = None
    Bairro: Optional[str] = None
    Cidade: str
    UF: str
    CEP: Optional[str] = None
    DDD: Optional[str] = None
    Telefone: Optional[str] = None
    Fax: Optional[str] = None
    Endereco_eletronico: Optional[str] = None
    Representante: Optional[str] = None
    Cargo_Representante: Optional[str] = None
    Regiao_de_Comercializacao: Optional[str] = None
    Data_Registro_ANS: Optional[date] = None

class OperadoraCreate(OperadoraBase):
    pass

class Operadora(OperadoraBase):
    id: int

    class Config:
        from_attributes = True  
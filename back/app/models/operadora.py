from sqlalchemy import Column, Integer, String, Date, Index
from ..database import Base

class Operadora(Base):
    __tablename__ = "operadoras"

    id = Column(Integer, primary_key=True, index=True)
    Registro_ANS = Column(String(20), index=True)
    CNPJ = Column(String(14), index=True, unique=True)
    Razao_Social = Column(String(255), index=True)
    Nome_Fantasia = Column(String(255))
    Modalidade = Column(String(100), index=True)
    Logradouro = Column(String(255))
    Numero = Column(String(50))
    Complemento = Column(String(255))
    Bairro = Column(String(100))
    Cidade = Column(String(100), index=True)
    UF = Column(String(2), index=True)
    CEP = Column(String(10))
    DDD = Column(String(5))
    Telefone = Column(String(20))
    Fax = Column(String(20))
    Endereco_eletronico = Column(String(255))
    Representante = Column(String(255))
    Cargo_Representante = Column(String(100))
    Regiao_de_Comercializacao = Column(String(10))
    Data_Registro_ANS = Column(Date)

    __table_args__ = (
        Index('idx_composite_search', 'UF', 'Cidade', 'Modalidade'),
    )
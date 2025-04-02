from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.operadora import Operadora as OperadoraModel
from ..schemas.operadora import Operadora
from ..database import get_db

router = APIRouter()

@router.get("/operadoras", response_model=List[Operadora])
def listar_operadoras(
    uf: Optional[str] = Query(None, max_length=2),
    cidade: Optional[str] = Query(None),
    modalidade: Optional[str] = Query(None),
    cnpj: Optional[str] = Query(None, max_length=14),
    razao_social: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(OperadoraModel)
    
    filters = []
    if uf:
        filters.append(OperadoraModel.UF == uf.upper())
    if cidade:
        filters.append(OperadoraModel.Cidade.ilike(f"%{cidade}%"))
    if modalidade:
        filters.append(OperadoraModel.Modalidade.ilike(f"%{modalidade}%"))
    if cnpj:
        filters.append(OperadoraModel.CNPJ == cnpj)
    if razao_social:
        filters.append(OperadoraModel.Razao_Social.ilike(f"%{razao_social}%"))
    
    if filters:
        query = query.filter(*filters)
    
    return query.offset(offset).limit(limit).all()
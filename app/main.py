from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Funcionario, Prefeitura, Contribuicao, Aposentadoria
from .schemas import FuncionarioOut
from sqlalchemy import func

app = FastAPI(title="RPPS API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/funcionarios/{cpf}", response_model=FuncionarioOut)
def get_funcionario_by_cpf(cpf: str, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@app.get("/relatorios/media-salario-por-prefeitura")
def media_salario_por_prefeitura(db: Session = Depends(get_db)):
    results = db.query(
        Prefeitura.nome,
        func.avg(Contribuicao.salario_contribuicao).label("media_salarial")
    ).join(Funcionario, Funcionario.id_prefeitura == Prefeitura.id
    ).join(Contribuicao, Contribuicao.id_funcionario == Funcionario.id
    ).group_by(Prefeitura.nome).all()

    return [{"prefeitura": r[0], "media_salarial": float(r[1])} for r in results]

@app.get("/relatorios/aposentadorias-por-tipo")
def aposentadorias_por_tipo(db: Session = Depends(get_db)):
    results = db.query(
        Aposentadoria.tipo,
        func.count(Aposentadoria.id)
    ).group_by(Aposentadoria.tipo).all()

    return [{"tipo": r[0], "quantidade": r[1]} for r in results]

@app.get("/relatorios/media-contribuicoes-por-mes")
def media_contribuicoes_por_mes(db: Session = Depends(get_db)):
    results = db.query(
        func.date_trunc('month', Contribuicao.competencia).label("mes"),
        func.avg(Contribuicao.contribuicao).label("media_contribuicao")
    ).group_by("mes").order_by("mes").all()

    return [{"mes": r[0].strftime("%Y-%m"), "media_contribuicao": float(r[1])} for r in results]

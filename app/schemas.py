from pydantic import BaseModel
from typing import Optional
from datetime import date

class FuncionarioBase(BaseModel):
    nome: str
    cpf: str
    cargo: Optional[str]
    sexo: str
    data_nascimento: date
    data_admissao: date
    regime_aposentadoria: str
    vinculo: str
    id_prefeitura: int

class FuncionarioOut(FuncionarioBase):
    id: int
    class Config:
        orm_mode = True

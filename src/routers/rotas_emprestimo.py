from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.schemas import Emprestimo
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.emprestimo_repo import RepositorioEmprestimo

router = APIRouter(prefix="/emprestimos")

@router.post('/add', response_model=Emprestimo)
def adicionar_emprestimo(emprestimo: Emprestimo, db: Session = Depends(get_db)):
    return RepositorioEmprestimo(db).criar(emprestimo)

@router.get('/all', response_model=List[Emprestimo])
def listar_emprestimos(db: Session = Depends(get_db)):
    return RepositorioEmprestimo(db).listar()

@router.get('/view/{emprestimo_id}', response_model=Emprestimo)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = RepositorioEmprestimo(db).obter_por_id(emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
    return emprestimo

@router.delete('/delete/{emprestimo_id}')
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    RepositorioEmprestimo(db).remover(emprestimo_id)
    return {'Msg': 'Empréstimo removido com sucesso'}

@router.put('/edit/{emprestimo_id}', response_model=Emprestimo)
def atualizar_emprestimo(emprestimo_id: int, emprestimo: Emprestimo, db: Session = Depends(get_db)):
    emprestimo.id = emprestimo_id
    return RepositorioEmprestimo(db).editar(emprestimo_id, emprestimo)

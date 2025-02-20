from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import EmprestimoSchema, LivroSchema, LivroSimplesSchema
from src.infra.sqlalchemy.repositorios.livro_repo import RepositorioLivro
from src.infra.sqlalchemy.repositorios.emprestimo_repo import RepositorioEmprestimo

router = APIRouter(prefix="/livro", tags=['livros'])

@router.post('/add', response_model=LivroSchema)
def adicionar_livro(livro: LivroSchema, db: Session = Depends(get_db)):
    return RepositorioLivro(db).criar(livro)

@router.get('/all', response_model=List[LivroSimplesSchema])
def listar(db: Session = Depends(get_db)):
    return RepositorioLivro(db).listar()

@router.get('/view/{livro_id}')
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro_encontrado = RepositorioLivro(db).obter_por_id(livro_id)
    if not livro_encontrado:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro_encontrado

@router.delete('/delete/{livro_id}')
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    RepositorioLivro(db).remover(livro_id)
    return {"Msg": "Livro removido com sucesso"}

@router.put('/edit/{livro_id}')
def atualizar_livro(livro_id: int, livro: LivroSchema, db: Session = Depends(get_db)):
    livro.id = livro_id
    RepositorioLivro(db).editar(livro_id, livro)
    return livro

@router.get('/emprestimos/{livro_id}', response_model=List[EmprestimoSchema])
def listar_emprestimos_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = RepositorioLivro(db).obter_por_id(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    return RepositorioEmprestimo(db).listar_por_livro(livro_id)
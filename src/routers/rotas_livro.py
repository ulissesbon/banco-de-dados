from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.schemas import Livro, LivroSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.livro_repo import RepositorioLivro

router = APIRouter(prefix="/livro")

@router.post('/add', response_model=Livro)
def adicionar_livro(livro: Livro, db: Session = Depends(get_db)):
    return RepositorioLivro(db).criar(livro)

@router.get('/all', response_model=List[LivroSimples])
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
def atualizar_livro(livro_id: int, livro: Livro, db: Session = Depends(get_db)):
    livro.id = livro_id
    RepositorioLivro(db).editar(livro_id, livro)
    return livro

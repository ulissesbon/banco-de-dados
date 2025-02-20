from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.schemas import Editora, EditoraSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.editora_repo import RepositorioEditora


router = APIRouter(prefix="/editora")


@router.post('/add', response_model=Editora)
def adicionar_editora(editora: Editora, db: Session = Depends(get_db)):
    return RepositorioEditora(db).criar(editora)

@router.get('/all', response_model=List[EditoraSimples])
def listar(db: Session = Depends(get_db)):
    return RepositorioEditora(db).listar()

@router.get('/view/{editora_id}')
def obter_editora(editora_id: int, db: Session = Depends(get_db)):
    editora_encontrada = RepositorioEditora(db).obter(editora_id)
    if not editora_encontrada:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return editora_encontrada

@router.delete('/delete/{editora_id}')
def deletar_editora(editora_id: int, db: Session = Depends(get_db)):
    RepositorioEditora(db).remover(editora_id)
    return {"Msg": "Editora removida com sucesso"}

@router.put('/edit/{editora_id}')
def atualizar_editora(editora_id: int, editora: Editora, db: Session = Depends(get_db)):
    editora.id = editora_id
    RepositorioEditora(db).editar(editora_id, editora)
    return editora

@router.get('/{editora_id}/livros', response_model=List[EditoraSimples])
def listar_livros_editora(editora_id: int, db: Session = Depends(get_db)):
    return RepositorioEditora(db).listar_livros(editora_id)

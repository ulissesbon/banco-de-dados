from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import Emprestimo, Usuario, UsuarioSimples
from src.infra.sqlalchemy.repositorios.usuario_repo import RepositorioUsuario
from src.infra.sqlalchemy.repositorios.emprestimo_repo import RepositorioEmprestimo

router = APIRouter(prefix="/usuarios")

@router.post('/add', response_model=UsuarioSimples)
def adicionar_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    usuario_localizado = RepositorioUsuario(db).obter_por_telefone(usuario.telefone)

    if usuario_localizado:
        raise HTTPException(status_code=400, detail='Usuário já existente')
    usuario_criado = RepositorioUsuario(db).criar(usuario)

    return usuario_criado

@router.get('/all', response_model=List[UsuarioSimples])
def listar(db: Session = Depends(get_db)):

    return RepositorioUsuario(db).listar()

@router.get('/view/{usuario_id}')
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_encontrado = RepositorioUsuario(db).obter(usuario_id)

    if not usuario_encontrado:
        return HTTPException(status_code=404)
    return usuario_encontrado.to_dict()

@router.delete('/delete/{usuario_id}')
def deletar_usuario(usuario_id: int, db: Session= Depends(get_db)):
    RepositorioUsuario(db).remover(usuario_id)

    return{'Msg': 'Usuario removido com sucesso'}

@router.put('/edit/{usuario_id}')
def atualizar_produto(usuario_id: int, usuario: Usuario, db: Session= Depends(get_db)):
    usuario.id = usuario_id
    RepositorioUsuario(db).editar(usuario_id, usuario)

    return usuario

@router.get('/emprestimos/{usuario_id}', response_model=List[Emprestimo])
def listar_emprestimos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = RepositorioUsuario(db).obter(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return RepositorioEmprestimo(db).listar_por_usuario(usuario_id)
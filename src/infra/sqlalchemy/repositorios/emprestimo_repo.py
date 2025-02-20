from src.schemas import schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from src.infra.sqlalchemy.models import models

class RepositorioEmprestimo():
    
    def __init__(self, db: Session):
        self.db = db

    def criar(self, emprestimo: schemas.EmprestimoSchema):
        db_emprestimo = models.Emprestimo(
            livro_id        = emprestimo.livro_id,
            usuario_id      = emprestimo.usuario_id,
            data_emprestimo = emprestimo.data_emprestimo,
            atraso          = emprestimo.atraso,
            multa           = emprestimo.multa
        )
        self.db.add(db_emprestimo)
        self.db.commit()
        self.db.refresh(db_emprestimo)
        return db_emprestimo

    def listar(self):
        stmt = select(models.Emprestimo)
        return self.db.execute(stmt).scalars().all()

    def obter_por_id(self, emprestimo_id: int):
        stmt = select(models.Emprestimo).filter_by(id=emprestimo_id)
        emprestimo = self.db.execute(stmt).scalar()
        if not emprestimo:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        return emprestimo

    def remover(self, emprestimo_id: int):
        stmt = delete(models.Emprestimo).where(models.Emprestimo.id == emprestimo_id)
        self.db.execute(stmt)
        self.db.commit()

    def editar(self, id_emprestimo: int, emprestimo: schemas.EmprestimoSchema):
        emprestimo_existente = self.db.query(models.Emprestimo).filter(models.Emprestimo.id == emprestimo.id).first()
        if not emprestimo_existente:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        
        update_stmt = update(models.Emprestimo).where(models.Emprestimo.id == id_emprestimo).values(
            livro_id        = emprestimo.livro_id,
            usuario_id      = emprestimo.usuario_id,
            data_emprestimo = emprestimo.data_emprestimo,
            atraso          = emprestimo.atraso,
            multa           = emprestimo.multa
        )
        self.db.execute(update_stmt)
        self.db.commit()

    def listar_por_usuario(self, usuario_id: int):
        stmt = select(models.Emprestimo).where(models.Emprestimo.usuario_id == usuario_id)
        emprestimos = self.db.execute(stmt).scalars().all()
        if not emprestimos:
            return []
        return emprestimos
    
    def listar_por_livro(self, livro_id: int):
        stmt = select(models.Emprestimo).where(models.Emprestimo.livro_id == livro_id)
        emprestimos = self.db.execute(stmt).scalars().all()
        if not emprestimos:
            return None
        return emprestimos
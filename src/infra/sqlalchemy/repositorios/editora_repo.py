from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioEditora():
    
    def __init__(self, db: Session):
        self.db = db


    def criar(self, editora: schemas.Editora):
        db_editora = models.Editora(
            nome        = editora.nome,
            telefone    = editora.telefone,
            logradouro  = editora.logradouro,
            numero      = editora.numero,
            cep         = editora.cep,
            bairro      = editora.bairro
            )
        
        self.db.add(db_editora)
        self.db.commit() 
        self.db.refresh(db_editora) 
        return db_editora


    def listar(self):
        stmt = select(models.Editora)
        editoras = self.db.execute(stmt).scalars().all()
        if not editoras:
            return None
        return editoras


    def obter(self, editora_id: int):
        stmt = select(models.Editora).filter_by(id= editora_id)
        editora = self.db.execute(stmt).scalar()

        return editora


    def obter_por_telefone(self, telefone: str) -> models.Editora:
        stmt = select(models.Editora).where(models.Editora.telefone == telefone)
        editora = self.db.execute(stmt).scalars().first()

        return editora


    def remover(self, editora_id: int):
        stmt = delete(models.Editora).where(models.Editora.id == editora_id)

        self.db.execute(stmt)
        self.db.commit()


    def editar(self, id_editora: int, editora: schemas.Editora):
        
        editora_existente = self.db.query(models.Editora).filter(models.Editora.id == editora.id).first()
        if not editora_existente:
            raise HTTPException(status_code=404, detail= "editora não encontrado")
        
        update_stmt = update(models.Editora
                             ).where(models.Editora.id == id_editora
                                     ).values(
                                            nome        = editora.nome,
                                            telefone    = editora.telefone,
                                            logradouro  = editora.logradouro,
                                            numero      = editora.numero,
                                            cep         = editora.cep,
                                            bairro      = editora.bairro
                                            )
        
        self.db.execute(update_stmt)
        self.db.commit()


    def listar_livros(self, editora_id: int):
        stmt = select(models.Livro).where(models.Livro.editora_id == editora_id)
        livros = self.db.execute(stmt).scalars().all()
        return livros
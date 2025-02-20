from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioLivro():
    
    def __init__(self, db: Session):
        self.db = db


    def criar(self, livro: models.Livro):
        db_livro = models.Livro(
            titulo      = livro.titulo,
            num_pags    = livro.num_pags,
            colecao     = livro.colecao,
            editora_id  = livro.editora_id
            )
        
        self.db.add(db_livro)
        self.db.commit() 
        self.db.refresh(db_livro) 
        return db_livro


    def listar(self):
        stmt = select(models.Livro)
        livros = self.db.execute(stmt).scalars().all()
        return livros


    def obter_por_id(self, livro_id: int):
        stmt = select(models.Livro).filter_by(id= livro_id)
        livro = self.db.execute(stmt).scalar()

        if not livro:
            raise HTTPException(status_code=404, detail= 'Livro não encontrado')

        return livro


    def remover(self, livro_id: int):
        stmt = delete(models.Livro).where(models.Livro.id == livro_id)

        self.db.execute(stmt)
        self.db.commit()


    def editar(self, id_livro: int, livro: schemas.LivroSchema):
        
        livro_existente = self.db.query(models.Livro).filter(models.Livro.id == livro.id).first()
        if not livro_existente:
            raise HTTPException(status_code=404, detail= "Livro não encontrado")
        
        update_stmt = update(models.Livro
                             ).where(models.Livro.id == id_livro
                                     ).values(
                                            titulo      = livro.titulo,
                                            num_pags    = livro.num_pags,
                                            colecao     = livro.colecao,
                                            editora_id  = livro.editora_id
                                            )
        
        self.db.execute(update_stmt)
        self.db.commit()


    
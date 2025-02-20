from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base
from sqlalchemy import Column, Date, Integer, String, Float, Boolean, ForeignKey

class Usuario(Base):
    __tablename__ = 'usuario'

    id          = Column(Integer, primary_key= True, index= True, autoincrement= True)
    nome        = Column(String)
    telefone    = Column(String)
    logradouro  = Column(String)
    numero      = Column(Integer)
    cep         = Column(String)
    bairro      = Column(String)

    emprestimos = relationship('Emprestimo', back_populates='usuario')


class Editora(Base):
    __tablename__ = 'editora'

    id          = Column(Integer, primary_key= True, index= True, autoincrement= True)
    nome        = Column(String)
    telefone    = Column(String)
    logradouro  = Column(String)
    numero      = Column(Integer)
    cep         = Column(String)
    bairro      = Column(String)

    livros      = relationship('Livro', back_populates= 'editora') 


class Livro(Base):
    __tablename__ = 'livro'

    id          = Column(Integer, primary_key= True, index= True, autoincrement= True)
    titulo      = Column(String)
    num_pags    = Column(Integer)
    colecao     = Column(String)

    emprestimos = relationship('Emprestimo', back_populates='livro')

    editora_id  = Column(Integer, ForeignKey('editora.id', name= 'fk_editora'))
    editora     = relationship('Editora', foreign_keys=[editora_id], back_populates= 'livros')


class Emprestimo(Base):
    __tablename__ = 'emprestimo'

    id              = Column(Integer, primary_key=True, index=True, autoincrement= True)
    livro_id        = Column(Integer, ForeignKey('livro.id', name='fk_livro'))
    usuario_id      = Column(Integer, ForeignKey('usuario.id', name='fk_usuario'))
    data_emprestimo = Column(Date)
    atraso          = Column(Boolean, default=False)
    multa           = Column(Float, nullable=True)

    livro           = relationship('Livro', back_populates='emprestimos')
    usuario         = relationship('Usuario', back_populates='emprestimos')
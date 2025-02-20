from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base
from sqlalchemy import Column, Date, Integer, String, Float, Boolean, ForeignKey

class Usuario(Base):
    __tablename__ = 'usuario'

    def __init__(self, nome: str, telefone: str, logradouro: str, numero: int, cep: str, bairro: str):
        self.nome = nome
        self.telefone = telefone
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.bairro = bairro

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
    
    def __init__(self, nome: str, telefone: str, logradouro: str, numero: int, cep: str, bairro: str):
        self.nome = nome
        self.telefone = telefone
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.bairro = bairro


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

    def __init__(self, titulo: str, num_pags: int, editora_id: int, colecao: str = None):
        self.titulo = titulo
        self.num_pags = num_pags
        self.colecao = colecao
        self.editora_id = editora_id

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
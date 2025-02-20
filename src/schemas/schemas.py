from datetime import date
from pydantic import BaseModel
from typing import Optional, List


class Usuario(BaseModel):
    id          : Optional[int] = None
    nome        : str
    telefone    : str
    logradouro  : str
    numero      : int
    cep         : str
    bairro      : str

    class Config:
        orm_mode = True

class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str

    class Config:
        orm_mode = True

class EditoraSimples(BaseModel):
    id          : Optional[int] = None
    nome        : str

    class Config:
        orm_mode = True

class LivroSimples(BaseModel):
    id              : Optional[int] = None
    titulo          : str
    editora_id      : int

    class Config:
        orm_mode = True

class Editora(BaseModel):
    id          : Optional[int] = None
    nome        : str
    telefone    : str
    logradouro  : str
    numero      : int
    cep         : str
    bairro      : str
    livros      : List[LivroSimples] = []

    class Config:
        orm_mode = True

class Livro(BaseModel):
    id              : Optional[int] = None
    titulo          : str
    num_pags        : int
    colecao         : Optional[str] = None
    editora_id      : int

    editora         : Optional[Editora] = None

    class Config:
        orm_mode = True

class Emprestimo(BaseModel):
    livro_id        : int
    usuario_id      : int
    data_emprestimo : date
    atraso          : Optional[bool] = False
    multa           : Optional[float] = None

    class Config:
        orm_mode = True
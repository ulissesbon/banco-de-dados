from datetime import date
from pydantic import BaseModel
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome        : str
    telefone    : str
    logradouro  : str
    numero      : int
    cep         : str
    bairro      : str

    class Config:
        orm_mode = True

class UsuarioSimplesSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str

    class Config:
        orm_mode = True

class LivroSimplesSchema(BaseModel):
    id              : Optional[int] = None
    titulo          : str
    editora_id      : int

    class Config:
        orm_mode = True

class EditoraSimplesSchema(BaseModel):
    id          : Optional[int] = None
    nome        : str
    livros      : List[LivroSimplesSchema] = []

    class Config:
        orm_mode = True

class ResponseEditoraSchema(BaseModel):
    id          : Optional[int] = None
    nome        : str
    telefone    : str
    cep         : str
    numero      : int
    livros      : List[LivroSimplesSchema] = []

    class Config:
        orm_mode = True

class EditoraSchema(BaseModel):
    nome        : str
    telefone    : str
    logradouro  : str
    numero      : int
    cep         : str
    bairro      : str

    class Config:
        orm_mode = True

class LivroSchema(BaseModel):
    titulo          : str
    num_pags        : int
    colecao         : Optional[str] = None
    editora_id      : Optional[int]

    class Config:
        orm_mode = True

class EmprestimoSchema(BaseModel):
    livro_id        : int
    usuario_id      : int
    data_emprestimo : date
    atraso          : Optional[bool] = False
    multa           : Optional[float] = None

    class Config:
        orm_mode = True
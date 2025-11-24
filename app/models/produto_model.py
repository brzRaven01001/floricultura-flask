# app/models/produto_model.py
from dataclasses import dataclass
from typing import List, Optional
from app.models.data_store import PRODUTOS


@dataclass
class Produto:
    id: int
    nome: str
    categoria: str
    preco: float
    imagem: str
    descricao: str


def _to_obj(dados: dict) -> Produto:
    return Produto(
        id=dados['id'],
        nome=dados['nome'],
        categoria=dados['categoria'],
        preco=dados['preco'],
        imagem=dados['imagem'],
        descricao=dados['descricao'],
    )


def listar_produtos_populares() -> List[Produto]:
    populares_ids = [1, 2, 3]
    return [_to_obj(p) for p in PRODUTOS.values() if p['id'] in populares_ids]


def listar_por_categoria(categoria: str) -> List[Produto]:
    return [_to_obj(p) for p in PRODUTOS.values() if p['categoria'] == categoria]


def listar_todos() -> List[Produto]:
    return [_to_obj(p) for p in PRODUTOS.values()]


def obter_produto(produto_id: int) -> Optional[Produto]:
    dados = PRODUTOS.get(produto_id)
    return _to_obj(dados) if dados else None

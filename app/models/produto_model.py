# app/models/produto_model.py
from dataclasses import dataclass
from typing import List, Optional
from app.models.data_store import PRODUTOS, salvar_dados

@dataclass
class Produto:
    id: int
    nome: str
    categoria: str
    preco: float
    imagem: str
    descricao: str
    quantidade: int # Campo obrigatório para o sistema funcionar

def _to_obj(dados: dict) -> Produto:
    """Converte um dicionário do banco em um Objeto Produto."""
    return Produto(
        id=dados['id'],
        nome=dados['nome'],
        categoria=dados['categoria'],
        preco=dados['preco'],
        imagem=dados['imagem'],
        descricao=dados['descricao'],
        # SEGURANÇA: Se não tiver 'quantidade' no banco, assume 0 para não travar
        quantidade=dados.get('quantidade', 0) 
    )

def listar_produtos_populares() -> List[Produto]:
    populares_ids = [1, 2, 3] # IDs que aparecem na Home
    return [_to_obj(p) for p in PRODUTOS.values() if p['id'] in populares_ids]

def listar_por_categoria(categoria: str) -> List[Produto]:
    return [_to_obj(p) for p in PRODUTOS.values() if p['categoria'] == categoria]

def listar_todos() -> List[Produto]:
    return [_to_obj(p) for p in PRODUTOS.values()]

def obter_produto(produto_id: int) -> Optional[Produto]:
    dados = PRODUTOS.get(produto_id)
    return _to_obj(dados) if dados else None

# --- FUNÇÕES DE CONTROLE DE ESTOQUE ---

def verificar_estoque(produto_id: int, quantidade_desejada: int) -> bool:
    """Verifica se tem produto suficiente antes de adicionar ao carrinho."""
    produto = obter_produto(produto_id)
    if produto and produto.quantidade >= quantidade_desejada:
        return True
    return False

def baixar_estoque(produto_id: int, quantidade_vendida: int):
    """Diminui a quantidade no banco após a compra."""
    if produto_id in PRODUTOS:
        PRODUTOS[produto_id]['quantidade'] -= quantidade_vendida
        salvar_dados()
# app/models/pedido_model.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from app.models.data_store import PEDIDOS, salvar_dados

@dataclass
class ItemPedido:
    id: int
    nome: str
    preco: float
    imagem: str
    quantidade: int

@dataclass
class Pedido:
    id: int
    cliente_email: str
    cliente_nome: str
    itens: List[ItemPedido]
    total: float
    data: str
    data_entrega: str
    status: str

def _item_from_dict(d: dict) -> ItemPedido:
    return ItemPedido(
        id=d['id'],
        nome=d['nome'],
        preco=d['preco'],
        imagem=d['imagem'],
        quantidade=d['quantidade']
    )

def _from_dict(d: dict) -> Pedido:
    itens = [_item_from_dict(i) for i in d['itens']]
    return Pedido(
        id=d['id'],
        cliente_email=d['cliente_email'],
        cliente_nome=d['cliente_nome'],
        itens=itens,
        total=d['total'],
        data=d['data'],
        data_entrega=d.get('data_entrega', 'Não informada'),
        status=d['status']
    )

def listar_pedidos_cliente(email: str) -> List[Pedido]:
    return [_from_dict(p) for p in PEDIDOS if p['cliente_email'] == email]

def listar_todos() -> List[Pedido]:
    return [_from_dict(p) for p in PEDIDOS]

# --- NOVA FUNÇÃO NECESSÁRIA PARA O CANCELAMENTO ---
def obter_pedido(pedido_id: int) -> Optional[Pedido]:
    for p in PEDIDOS:
        if p['id'] == pedido_id:
            return _from_dict(p)
    return None
# --------------------------------------------------

def criar_pedido(cliente_email: str, cliente_nome: str, itens_carrinho: List[dict], data_entrega: str) -> Pedido:
    novo_id = len(PEDIDOS) + 1
    total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

    pedido_dict = {
        'id': novo_id,
        'cliente_email': cliente_email,
        'cliente_nome': cliente_nome,
        'itens': itens_carrinho.copy(),
        'total': total,
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'data_entrega': data_entrega,
        'status': 'Confirmado'
    }
    
    PEDIDOS.append(pedido_dict)
    salvar_dados()

    return _from_dict(pedido_dict)

def alterar_status(pedido_id: int, novo_status: str):
    for p in PEDIDOS:
        if p['id'] == pedido_id:
            p['status'] = novo_status
            salvar_dados()
            return _from_dict(p)
    return None

def calcular_faturamento_total():
    return sum(p['total'] for p in PEDIDOS)
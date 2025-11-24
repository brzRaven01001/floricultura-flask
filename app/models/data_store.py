# app/models/data_store.py
import json

USUARIOS = {
    'admin@floricultura.com': {
        'senha': '123456',
        'nome': 'Administrador',
        'tipo': 'admin',
        'telefone': '(11) 99999-9999'
    },
    'cliente@email.com': {
        'senha': '123456',
        'nome': 'João Cliente',
        'tipo': 'cliente',
        'telefone': '(11) 88888-8888'
    }
}

PRODUTOS = {
    1: {
        'id': 1,
        'nome': 'Buquê de Rosas Vermelhas',
        'categoria': 'buques',
        'preco': 120.00,
        'imagem': 'lindo-buque-de-flores.jpg',
        'descricao': 'Lindo buquê com 12 rosas vermelhas frescas e aromáticas'
    },
    2: {
        'id': 2,
        'nome': 'Arranjo de Girassóis',
        'categoria': 'arranjos',
        'preco': 85.00,
        'imagem': 'lindo-arranjo.jpg',
        'descricao': 'Arranjo vibrante com girassóis que trazem alegria ao ambiente'
    },
    3: {
        'id': 3,
        'nome': 'Buquê de Margaridas',
        'categoria': 'buques',
        'preco': 65.00,
        'imagem': 'um-lindo-buque.jpg',
        'descricao': 'Buquê delicado com margaridas brancas e verdes'
    },
    4: {
        'id': 4,
        'nome': 'Kit Aniversário Premium',
        'categoria': 'aniversario',
        'preco': 150.00,
        'imagem': 'Kit_Aniversario1.jpg',
        'descricao': 'Kit completo para aniversário com flores variadas'
    },
    5: {
        'id': 5,
        'nome': 'Arranjo de Orquídeas',
        'categoria': 'arranjos',
        'preco': 95.00,
        'imagem': 'Kit_Aniversario2.jpg',
        'descricao': 'Elegante arranjo com orquídeas brancas e roxas'
    },
    6: {
        'id': 6,
        'nome': 'Buquê de Lírios',
        'categoria': 'buques',
        'preco': 110.00,
        'imagem': 'Kit_Aniversario3.jpg',
        'descricao': 'Buquê sofisticado com lírios brancos e verdes'
    },
    7: {
        'id': 7,
        'nome': 'Coroa de Flores Brancas',
        'categoria': 'coroa',
        'preco': 130.00,
        'imagem': 'Kit_Aniversario4.jpg',
        'descricao': 'Coroa elegante com flores brancas para ocasiões especiais'
    },
    8: {
        'id': 8,
        'nome': 'Kit Romântico Premium',
        'categoria': 'kit_romantico',
        'preco': 180.00,
        'imagem': 'Kit_Aniversario5.jpg',
        'descricao': 'Kit romântico com rosas vermelhas e chocolates'
    }
}

PEDIDOS = []


def salvar_dados():
    dados = {
        'usuarios': USUARIOS,
        'pedidos': PEDIDOS,
        'produtos': PRODUTOS
    }
    with open('dados.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_dados():
    global USUARIOS, PEDIDOS, PRODUTOS
    try:
        with open('dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            USUARIOS = dados.get('usuarios', USUARIOS)
            PEDIDOS = dados.get('pedidos', PEDIDOS)
            PRODUTOS = dados.get('produtos', PRODUTOS)
    except FileNotFoundError:
        pass


carregar_dados()

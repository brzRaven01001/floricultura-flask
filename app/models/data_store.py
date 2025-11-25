# app/models/data_store.py
import json

# Usuários para Login
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

# Banco de Dados de Produtos
# IMPORTANTE: Mantenha os IDs (1, 2, 3, 6, 7, 8) pois seus HTMLs usam eles.
PRODUTOS = {
    1: {
        'id': 1,
        'nome': 'Buquê de Rosas Vermelhas',
        'categoria': 'buques',
        'preco': 120.00,
        'imagem': 'lindo-buque-de-flores.jpg',
        'descricao': 'Lindo buquê com 12 rosas vermelhas frescas e aromáticas',
        'quantidade': 10
    },
    2: {
        'id': 2,
        'nome': 'Arranjo de Girassóis',
        'categoria': 'arranjos',
        'preco': 85.00,
        'imagem': 'lindo-arranjo.jpg',
        'descricao': 'Arranjo vibrante com girassóis que trazem alegria ao ambiente',
        'quantidade': 5
    },
    3: {
        'id': 3,
        'nome': 'Orquídea Phalaenopsis',
        'categoria': 'arranjos',
        'preco': 150.00,
        'imagem': 'Kit_Aniversario2.jpg',
        'descricao': 'Elegante arranjo com orquídeas brancas e roxas',
        'quantidade': 3
    },
    6: {
        'id': 6,
        'nome': 'Buquê de Lírios',
        'categoria': 'buques',
        'preco': 110.00,
        'imagem': 'Kit_Aniversario3.jpg',
        'descricao': 'Buquê sofisticado com lírios brancos e verdes',
        'quantidade': 8
    },
    7: {
        'id': 7,
        'nome': 'Coroa de Flores Brancas',
        'categoria': 'coroa',
        'preco': 130.00,
        'imagem': 'Kit_Aniversario4.jpg',
        'descricao': 'Coroa elegante com flores brancas para ocasiões especiais',
        'quantidade': 2
    },
    8: {
        'id': 8,
        'nome': 'Kit Romântico Premium',
        'categoria': 'kit_romantico',
        'preco': 180.00,
        'imagem': 'Kit_Aniversario5.jpg',
        'descricao': 'Kit romântico com rosas vermelhas e chocolates',
        'quantidade': 10
    }
}

PEDIDOS = []

def salvar_dados():
    pass
# app/models/usuario_model.py
from dataclasses import dataclass
from typing import Optional, List
from app.models.data_store import USUARIOS, salvar_dados


@dataclass
class Usuario:
    email: str
    senha: str
    nome: str
    tipo: str
    telefone: str


def autenticar(email: str, senha: str) -> Optional[Usuario]:
    dados = USUARIOS.get(email)
    if dados and dados['senha'] == senha:
        return Usuario(
            email=email,
            senha=dados['senha'],
            nome=dados['nome'],
            tipo=dados['tipo'],
            telefone=dados['telefone']
        )
    return None


def email_existe(email: str) -> bool:
    return email in USUARIOS


def criar_usuario(email: str, nome: str, senha: str, telefone: str) -> Usuario:
    USUARIOS[email] = {
        'senha': senha,
        'nome': nome,
        'tipo': 'cliente',
        'telefone': telefone
    }
    salvar_dados()
    return Usuario(
        email=email,
        senha=senha,
        nome=nome,
        tipo='cliente',
        telefone=telefone
    )


def listar_clientes() -> List[Usuario]:
    clientes = []
    for email, dados in USUARIOS.items():
        if dados['tipo'] == 'cliente':
            clientes.append(
                Usuario(
                    email=email,
                    senha=dados['senha'],
                    nome=dados['nome'],
                    tipo=dados['tipo'],
                    telefone=dados['telefone']
                )
            )
    return clientes

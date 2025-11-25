# app/views/admin_views.py
from flask import render_template, redirect, url_for, flash, session
from functools import wraps # Importante para criar o decorador
from app.models.pedido_model import (
    listar_todos as listar_todos_pedidos,
    alterar_status,
    calcular_faturamento_total
)
from app.models.usuario_model import listar_clientes
from app.models.produto_model import listar_todos as listar_todos_produtos


# --- DECORADOR DE SEGURANÇA (A Mágica acontece aqui) ---
def admin_required(f):
    """
    Protege as rotas.
    1. Se não tiver logado -> vai pro Login.
    2. Se tiver logado mas não for admin -> vai pra Home com ERRO.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Caso 1: Usuário nem está logado
        if 'user_email' not in session:
            flash('Você precisa fazer login para acessar essa área.', 'info')
            return redirect(url_for('login'))
        
        # Caso 2: Usuário está logado, mas NÃO é admin (O que você pediu)
        if session.get('user_type') != 'admin':
            flash('Atenção: Somente administradores podem acessar essa página!', 'error')
            return redirect(url_for('home')) # Manda para a home, não para o login
        
        # Caso 3: É admin, deixa passar
        return f(*args, **kwargs)
    return decorated_function
# -------------------------------------------------------


def init_admin_routes(app):
    
    # === DASHBOARD ADMIN ===
    @app.route('/admin/dashboard')
    @admin_required # <--- Aplica a segurança
    def admin_dashboard():
        
        pedidos = listar_todos_pedidos()
        total_pedidos = len(pedidos)
        total_clientes = len(listar_clientes())
        faturamento_total = calcular_faturamento_total()

        ultimos_pedidos = pedidos[-5:]

        return render_template(
            'dashboard.html', # Confirme se o nome do arquivo é esse mesmo
            total_pedidos=total_pedidos,
            total_clientes=total_clientes,
            faturamento_total=faturamento_total,
            pedidos=ultimos_pedidos
        )

    # === LISTA DE PEDIDOS ===
    @app.route('/admin/pedidos')
    @admin_required # <--- Aplica a segurança
    def admin_pedidos():
        pedidos = listar_todos_pedidos()
        return render_template('admin_pedidos.html', pedidos=pedidos)

    # === ALTERAR STATUS DO PEDIDO ===
    @app.route('/admin/alterar_status/<int:pedido_id>/<novo_status>')
    @admin_required # <--- Aplica a segurança
    def alterar_status_pedido(pedido_id, novo_status):
        pedido = alterar_status(pedido_id, novo_status)
        if pedido:
            flash(f'Status do pedido #{pedido_id} alterado para {novo_status}!', 'success')
        else:
            flash('Pedido não encontrado!', 'error')

        return redirect(url_for('admin_pedidos'))

    # === LISTA DE PRODUTOS ===
    @app.route('/admin/produtos')
    @admin_required # <--- Aplica a segurança
    def admin_produtos():
        produtos = listar_todos_produtos()
        return render_template('admin_produtos.html', produtos=produtos)
# app/views/admin_views.py
from flask import render_template, redirect, url_for, flash, session
from app.models.pedido_model import (
    listar_todos as listar_todos_pedidos,
    alterar_status,
    calcular_faturamento_total
)
from app.models.usuario_model import listar_clientes
from app.models.produto_model import listar_todos as listar_todos_produtos


def init_admin_routes(app):

    def is_admin():
        return 'user_email' in session and session.get('user_type') == 'admin'

    # === DASHBOARD ADMIN (rota que você mandou) ===
    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not is_admin():
            flash('Acesso restrito a administradores!', 'error')
            return redirect(url_for('login'))

        pedidos = listar_todos_pedidos()
        total_pedidos = len(pedidos)
        total_clientes = len(listar_clientes())
        faturamento_total = calcular_faturamento_total()

        # Últimos 5 pedidos (igual ao seu código antigo)
        ultimos_pedidos = pedidos[-5:]

        return render_template(
            'admin_dashboard.html',
            total_pedidos=total_pedidos,
            total_clientes=total_clientes,
            faturamento_total=faturamento_total,
            pedidos=ultimos_pedidos
        )

    # === LISTA DE PEDIDOS ===
    @app.route('/admin/pedidos')
    def admin_pedidos():
        if not is_admin():
            flash('Acesso restrito a administradores!', 'error')
            return redirect(url_for('login'))

        pedidos = listar_todos_pedidos()
        return render_template('admin_pedidos.html', pedidos=pedidos)

    # === ALTERAR STATUS DO PEDIDO ===
    @app.route('/admin/alterar_status/<int:pedido_id>/<novo_status>')
    def alterar_status_pedido(pedido_id, novo_status):
        if not is_admin():
            return redirect(url_for('login'))

        pedido = alterar_status(pedido_id, novo_status)
        if pedido:
            flash(f'Status do pedido #{pedido_id} alterado para {novo_status}!', 'success')
        else:
            flash('Pedido não encontrado!', 'error')

        return redirect(url_for('admin_pedidos'))

    # === LISTA DE PRODUTOS ===
    @app.route('/admin/produtos')
    def admin_produtos():
        if not is_admin():
            flash('Acesso restrito a administradores!', 'error')
            return redirect(url_for('login'))

        produtos = listar_todos_produtos()
        return render_template('admin_produtos.html', produtos=produtos)

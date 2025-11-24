# app/views/cliente_views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.models.pedido_model import listar_pedidos_cliente, criar_pedido
from app.models.produto_model import obter_produto

def init_cliente_routes(app):

    @app.route('/historico')
    def historico():
        if 'user_email' not in session:
            flash('Faça login para acessar seu histórico!', 'error')
            return redirect(url_for('login'))

        pedidos_usuario = listar_pedidos_cliente(session['user_email'])
        return render_template('historico_user.html', pedidos=pedidos_usuario)

    @app.route('/carrinho')
    def carrinho():
        if 'user_email' not in session:
            flash('Faça login para acessar o carrinho!', 'error')
            return redirect(url_for('login'))

        carrinho_usuario = session.get('carrinho', [])
        total = sum(item['preco'] * item['quantidade'] for item in carrinho_usuario)
        return render_template('carrinho.html', carrinho=carrinho_usuario, total=total)

    @app.route('/adicionar_carrinho/<int:produto_id>')
    def adicionar_carrinho(produto_id):
        if 'user_email' not in session:
            flash('Faça login para adicionar itens ao carrinho!', 'error')
            return redirect(url_for('login'))

        produto = obter_produto(produto_id)
        if produto:
            carrinho = session.get('carrinho', [])

            item_existente = next((item for item in carrinho if item['id'] == produto_id), None)

            if item_existente:
                item_existente['quantidade'] += 1
            else:
                carrinho.append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'preco': produto.preco,
                    'imagem': produto.imagem,
                    'quantidade': 1
                })

            session['carrinho'] = carrinho
            flash(f'{produto.nome} adicionado ao carrinho!', 'success')

        return redirect(request.referrer or url_for('home'))

    @app.route('/remover_carrinho/<int:produto_id>')
    def remover_carrinho(produto_id):
        if 'user_email' not in session:
            return redirect(url_for('login'))

        carrinho = session.get('carrinho', [])
        carrinho = [item for item in carrinho if item['id'] != produto_id]
        session['carrinho'] = carrinho
        flash('Item removido do carrinho!', 'success')

        return redirect(url_for('carrinho'))

    @app.route('/finalizar_pedido')
    def finalizar_pedido():
        if 'user_email' not in session:
            return redirect(url_for('login'))

        carrinho = session.get('carrinho', [])
        if not carrinho:
            flash('Seu carrinho está vazio!', 'error')
            return redirect(url_for('carrinho'))

        pedido = criar_pedido(
            cliente_email=session['user_email'],
            cliente_nome=session['user_name'],
            itens_carrinho=carrinho
        )

        # limpa carrinho
        session['carrinho'] = []

        flash(f'Pedido #{pedido.id} realizado com sucesso! Total: R$ {pedido.total:.2f}', 'success')
        return redirect(url_for('historico'))

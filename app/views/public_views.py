# app/views/public_views.py
from flask import render_template, flash, redirect, url_for
from app.models.produto_model import (
    listar_produtos_populares,
    listar_por_categoria,
    obter_produto
)

def init_public_routes(app):

    @app.route('/')
    def home():
        produtos_populares = listar_produtos_populares()
        return render_template('index.html', produtos_populares=produtos_populares)

    # --- ROTAS DE CATEGORIA ---
    @app.route('/produtos/aniversario')
    def produtos_aniversario():
        produtos = listar_por_categoria('aniversario')
        return render_template('aniversario.html', produtos=produtos)

    @app.route('/produtos/arranjos')
    def produtos_arranjos():
        produtos = listar_por_categoria('arranjos')
        return render_template('arranjos.html', produtos=produtos)

    @app.route('/produtos/buques')
    def produtos_buques():
        produtos = listar_por_categoria('buques')
        return render_template('buques.html', produtos=produtos)

    @app.route('/produtos/coroa')
    def produtos_coroa():
        produtos = listar_por_categoria('coroa')
        return render_template('coroa.html', produtos=produtos)

    @app.route('/produtos/kit_romantico')
    def produtos_kit_romantico():
        produtos = listar_por_categoria('kit_romantico')
        return render_template('kit_romantico.html', produtos=produtos)

    # --- ROTA DE DETALHES ---
    @app.route('/produto/<int:produto_id>')
    def ver_produto(produto_id):
        produto = obter_produto(produto_id)
        
        # Se o produto não for encontrado, redireciona para a home
        if produto is None:
            flash('Produto não encontrado ou indisponível.', 'error')
            return redirect(url_for('home'))

        return render_template('detalhes_produtos.html', produto=produto)
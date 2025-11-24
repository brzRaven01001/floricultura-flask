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

    @app.route('/produtos/aniversario')
    def produtos_aniversario():
        produtos_categoria = listar_por_categoria('aniversario')
        return render_template('aniversario.html', produtos=produtos_categoria)

    @app.route('/produtos/arranjos')
    def produtos_arranjos():
        produtos_categoria = listar_por_categoria('arranjos')
        return render_template('arranjos.html', produtos=produtos_categoria)

    @app.route('/produtos/buques')
    def produtos_buques():
        produtos_categoria = listar_por_categoria('buques')
        return render_template('buques.html', produtos=produtos_categoria)

    @app.route('/produtos/coroa')
    def produtos_coroa():
        produtos_categoria = listar_por_categoria('coroa')
        return render_template('coroa.html', produtos=produtos_categoria)

    @app.route('/produtos/kit_romantico')
    def produtos_kit_romantico():
        produtos_categoria = listar_por_categoria('kit_romantico')
        return render_template('kit_romantico.html', produtos=produtos_categoria)

    @app.route('/produto/<int:produto_id>')
    def ver_produto(produto_id):
        produto = obter_produto(produto_id)
        if not produto:
            flash('Produto não encontrado!', 'error')
            return redirect(url_for('home'))
        return render_template('detalhes_produto.html', produto=produto)

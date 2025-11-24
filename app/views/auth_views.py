# app/views/auth_views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.models.usuario_model import autenticar, email_existe, criar_usuario

def init_auth_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            usuario = autenticar(email, senha)
            if usuario:
                session['user_email'] = usuario.email
                session['user_name'] = usuario.nome
                session['user_type'] = usuario.tipo
                flash(f'Bem-vindo, {usuario.nome}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Email ou senha incorretos!', 'error')

        return render_template('login.html')

    @app.route('/criar_conta', methods=['GET', 'POST'])
    def criar_conta():
        if request.method == 'POST':
            email = request.form.get('email')
            nome = request.form.get('nome')
            senha = request.form.get('senha')
            telefone = request.form.get('telefone')

            if email_existe(email):
                flash('Email já cadastrado!', 'error')
            else:
                criar_usuario(email, nome, senha, telefone)
                flash('Conta criada com sucesso! Faça login.', 'success')
                return redirect(url_for('login'))

        return render_template('criar_conta.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logout realizado com sucesso!', 'success')
        return redirect(url_for('home'))

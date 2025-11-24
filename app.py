from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'flor_key_2024'

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

# Funções auxiliares
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

# Carregar dados ao iniciar
carregar_dados()

# ========== ROTAS PÚBLICAS ==========
@app.route('/')
def home():
    produtos_populares = [produto for produto in PRODUTOS.values() if produto['id'] in [1, 2, 3]]
    return render_template('index.html', produtos_populares=produtos_populares)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if email in USUARIOS and USUARIOS[email]['senha'] == senha:
            session['user_email'] = email
            session['user_name'] = USUARIOS[email]['nome']
            session['user_type'] = USUARIOS[email]['tipo']
            flash(f'Bem-vindo, {USUARIOS[email]["nome"]}!', 'success')
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
        
        if email in USUARIOS:
            flash('Email já cadastrado!', 'error')
        else:
            USUARIOS[email] = {
                'senha': senha,
                'nome': nome,
                'tipo': 'cliente',
                'telefone': telefone
            }
            salvar_dados()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('criar_conta.html')

# Rotas de produtos (públicas) - SEM verificação de login
@app.route('/produtos/aniversario')
def produtos_aniversario():
    produtos_categoria = [p for p in PRODUTOS.values() if p['categoria'] == 'aniversario']
    return render_template('aniversario.html', produtos=produtos_categoria)

@app.route('/produtos/arranjos')
def produtos_arranjos():
    produtos_categoria = [p for p in PRODUTOS.values() if p['categoria'] == 'arranjos']
    return render_template('arranjos.html', produtos=produtos_categoria)

@app.route('/produtos/buques')
def produtos_buques():
    produtos_categoria = [p for p in PRODUTOS.values() if p['categoria'] == 'buques']
    return render_template('buques.html', produtos=produtos_categoria)

@app.route('/produtos/coroa')
def produtos_coroa():
    produtos_categoria = [p for p in PRODUTOS.values() if p['categoria'] == 'coroa']
    return render_template('coroa.html', produtos=produtos_categoria)

@app.route('/produtos/kit_romantico')
def produtos_kit_romantico():
    produtos_categoria = [p for p in PRODUTOS.values() if p['categoria'] == 'kit_romantico']
    return render_template('kit_romantico.html', produtos=produtos_categoria)

@app.route('/produto/<int:produto_id>')
def ver_produto(produto_id):
    produto = PRODUTOS.get(produto_id)
    if not produto:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('home'))
    return render_template('detalhes_produto.html', produto=produto)

# ========== ROTAS PRIVADAS (requer login) ==========
@app.route('/historico')
def historico():
    if 'user_email' not in session:
        flash('Faça login para acessar seu histórico!', 'error')
        return redirect(url_for('login'))
    
    pedidos_usuario = [p for p in PEDIDOS if p['cliente_email'] == session['user_email']]
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
    
    produto = PRODUTOS.get(produto_id)
    if produto:
        carrinho = session.get('carrinho', [])
        
        # Verifica se o produto já está no carrinho
        item_existente = next((item for item in carrinho if item['id'] == produto_id), None)
        
        if item_existente:
            item_existente['quantidade'] += 1
        else:
            carrinho.append({
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'imagem': produto['imagem'],
                'quantidade': 1
            })
        
        session['carrinho'] = carrinho
        flash(f'{produto["nome"]} adicionado ao carrinho!', 'success')
    
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
    
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)
    
    pedido = {
        'id': len(PEDIDOS) + 1,
        'cliente_email': session['user_email'],
        'cliente_nome': session['user_name'],
        'itens': carrinho.copy(),
        'total': total,
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'status': 'Confirmado'
    }
    
    PEDIDOS.append(pedido)
    salvar_dados()
    
    # Limpa o carrinho
    session['carrinho'] = []
    
    flash(f'Pedido #{pedido["id"]} realizado com sucesso! Total: R$ {total:.2f}', 'success')
    return redirect(url_for('historico'))

# ========== ROTAS ADMINISTRATIVAS ==========
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_email' not in session or session.get('user_type') != 'admin':
        flash('Acesso restrito a administradores!', 'error')
        return redirect(url_for('login'))
    
    total_pedidos = len(PEDIDOS)
    total_clientes = len([u for u in USUARIOS.values() if u['tipo'] == 'cliente'])
    faturamento_total = sum(p['total'] for p in PEDIDOS)
    
    return render_template('admin_dashboard.html', 
                         total_pedidos=total_pedidos,
                         total_clientes=total_clientes,
                         faturamento_total=faturamento_total,
                         pedidos=PEDIDOS[-5:])  # Últimos 5 pedidos

@app.route('/admin/pedidos')
def admin_pedidos():
    if 'user_email' not in session or session.get('user_type') != 'admin':
        flash('Acesso restrito a administradores!', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin_pedidos.html', pedidos=PEDIDOS)

@app.route('/admin/alterar_status/<int:pedido_id>/<novo_status>')
def alterar_status_pedido(pedido_id, novo_status):
    if 'user_email' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    pedido = next((p for p in PEDIDOS if p['id'] == pedido_id), None)
    if pedido:
        pedido['status'] = novo_status
        salvar_dados()
        flash(f'Status do pedido #{pedido_id} alterado para {novo_status}!', 'success')
    
    return redirect(url_for('admin_pedidos'))

@app.route('/admin/produtos')
def admin_produtos():
    if 'user_email' not in session or session.get('user_type') != 'admin':
        flash('Acesso restrito a administradores!', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin_produtos.html', produtos=PRODUTOS.values())

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
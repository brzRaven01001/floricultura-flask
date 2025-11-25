# app/views/cliente_views.py
from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from app.models.pedido_model import listar_pedidos_cliente, criar_pedido, obter_pedido, alterar_status
from app.models.produto_model import obter_produto, verificar_estoque, baixar_estoque

def init_cliente_routes(app):

    @app.route('/historico')
    def historico():
        if 'user_email' not in session:
            flash('Faça login para acessar seu histórico!', 'error')
            return redirect(url_for('login'))

        pedidos_usuario = listar_pedidos_cliente(session['user_email'])
        # Invertendo a lista para mostrar os mais recentes primeiro
        return render_template('historico_user.html', pedidos=pedidos_usuario[::-1])

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
        if not produto:
            return redirect(url_for('home'))

        carrinho = session.get('carrinho', [])
        
        item_existe = False
        for item in carrinho:
            if item['id'] == produto_id:
                if verificar_estoque(produto_id, item['quantidade'] + 1):
                    item['quantidade'] += 1
                    flash(f'Mais uma unidade de {produto.nome} adicionada!', 'success')
                else:
                    flash(f'Estoque insuficiente para {produto.nome}!', 'error')
                item_existe = True
                break
        
        if not item_existe:
            if verificar_estoque(produto_id, 1):
                carrinho.append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'preco': produto.preco,
                    'imagem': produto.imagem,
                    'quantidade': 1
                })
                flash(f'{produto.nome} adicionado ao carrinho!', 'success')
            else:
                flash(f'Produto {produto.nome} esgotado!', 'error')

        session['carrinho'] = carrinho
        return redirect(request.referrer or url_for('home'))

    @app.route('/remover_carrinho/<int:produto_id>')
    def remover_carrinho(produto_id):
        if 'user_email' not in session: return redirect(url_for('login'))
        carrinho = session.get('carrinho', [])
        carrinho = [item for item in carrinho if item['id'] != produto_id]
        session['carrinho'] = carrinho
        flash('Item removido!', 'success')
        return redirect(url_for('carrinho'))

    @app.route('/finalizar_pedido', methods=['POST'])
    def finalizar_pedido():
        if 'user_email' not in session: return redirect(url_for('login'))
        carrinho = session.get('carrinho', [])
        if not carrinho: return redirect(url_for('carrinho'))

        data_str = request.form.get('data_entrega')
        
        try:
            data_entrega = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')
            agora = datetime.now()
            
            # RN03: Mínimo 24 horas de antecedência
            if data_entrega < (agora + timedelta(hours=24)):
                flash('A entrega deve ser agendada com no mínimo 24h de antecedência.', 'error')
                return redirect(url_for('carrinho'))

        except ValueError:
            flash('Data inválida.', 'error')
            return redirect(url_for('carrinho'))

        for item in carrinho:
            if not verificar_estoque(item['id'], item['quantidade']):
                flash(f'O produto {item["nome"]} acabou.', 'error')
                return redirect(url_for('carrinho'))

        data_formatada = data_entrega.strftime('%d/%m/%Y %H:%M')
        
        criar_pedido(
            cliente_email=session['user_email'],
            cliente_nome=session['user_name'],
            itens_carrinho=carrinho,
            data_entrega=data_formatada
        )

        for item in carrinho:
            baixar_estoque(item['id'], item['quantidade'])

        session.pop('carrinho')
        flash(f'Pedido agendado com sucesso para {data_formatada}!', 'success')
        return redirect(url_for('historico'))

    # --- NOVA ROTA: CANCELAMENTO COM REGRA DE 12 HORAS (RN06) ---
    @app.route('/cancelar_pedido/<int:pedido_id>')
    def cancelar_pedido(pedido_id):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        
        # 1. Busca o pedido
        pedido = obter_pedido(pedido_id)
        
        # 2. Segurança: Verifica se o pedido existe e é desse usuário
        if not pedido or pedido.cliente_email != session['user_email']:
            flash('Pedido não encontrado.', 'error')
            return redirect(url_for('historico'))
        
        # 3. Verifica se já não foi enviado ou cancelado
        if pedido.status != 'Confirmado':
            flash('Este pedido não pode mais ser cancelado.', 'error')
            return redirect(url_for('historico'))

        # 4. REGRA DE NEGÓCIO: Validação das 12 horas
        try:
            # Converte a string "25/11/2023 14:00" de volta para objeto Data
            data_entrega = datetime.strptime(pedido.data_entrega, '%d/%m/%Y %H:%M')
            agora = datetime.now()
            
            # Se (Entrega - Agora) for menor que 12 horas, ERRO.
            tempo_restante = data_entrega - agora
            
            if tempo_restante < timedelta(hours=12):
                flash('Cancelamento negado: Faltam menos de 12 horas para a entrega.', 'error')
            else:
                alterar_status(pedido_id, 'Cancelado')
                flash('Pedido cancelado com sucesso.', 'success')
                
        except Exception as e:
            flash(f'Erro ao validar data: {e}', 'error')

        return redirect(url_for('historico'))
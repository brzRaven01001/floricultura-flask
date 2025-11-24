from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'flor_key_2024'

    # IMPORTA AS ROTAS
    from app.views.public_views import init_public_routes
    from app.views.auth_views import init_auth_routes
    from app.views.cliente_views import init_cliente_routes
    from app.views.admin_views import init_admin_routes

    # REGISTRA AS ROTAS
    init_public_routes(app)
    init_auth_routes(app)
    init_cliente_routes(app)
    init_admin_routes(app)

    return app

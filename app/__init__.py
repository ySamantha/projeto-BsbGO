import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# A linha foi REMOVIDA daqui

def create_app():
    """
    Função que cria e configura a aplicação Flask (Application Factory).
    """
    app = Flask(__name__)

    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # E foi ADICIONADA AQUI, no local correto
    login_manager.login_view = 'main.login' # type: ignore

    # Importa o modelo de usuário para o loader
    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importa e registra o Blueprint com as rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
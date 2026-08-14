import os
from flask import Flask
from database import db
from controllers.usuario_controller import usuario_bp
from controllers.chamado_controller import chamado_bp

app = Flask(__name__)

# Configuração do SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "helpdesk.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do Banco
db.init_app(app)

# Registro das Blueprints (Rotas)
app.register_blueprint(usuario_bp)
app.register_blueprint(chamado_bp)

# Criação automática das tabelas SQLite ao iniciar
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
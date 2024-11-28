from flask import Flask
from flask_cors import CORS
from ext import db, jwt
import routes

def create_app():
    app = Flask(__name__)
    
    # Configurações do app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"
    
    # Inicialização de extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Registro de Blueprints
    app.register_blueprint(routes.routes)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados
    app.run(debug=True)
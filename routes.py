from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from ext import db
from models import Produto

routes = Blueprint("routes", __name__)

# Rota de autenticação
@routes.route("/login", methods=["POST"])
def login():
    """Autenticação de usuário."""
    dados = request.json
    username = dados.get("username")
    password = dados.get("password")
    
    if username == "admin" and password == "1234":
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    return jsonify(message="Credenciais inválidas"), 401

# Rota para listar produtos
@routes.route("/produtos", methods=["GET"])
@jwt_required()
def listar_produtos():
    """Lista todos os produtos."""
    try:
        print("Tentando listar produtos...")  # Log de início da função
        produtos = Produto.query.all()
        print(f"Produtos encontrados: {produtos}")  # Log dos produtos encontrados
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        # Log da exceção para depuração
        print(f"Erro ao listar produtos: {e}")
        return jsonify(message="Erro ao listar produtos"), 500

# Rota para criar um produto
@routes.route("/produtos", methods=["POST"])
@jwt_required()
def criar_produto():
    """Cria um novo produto."""
    dados = request.json
    
    # Validação de entrada
    if not all(k in dados for k in ["nome", "preco", "categoria", "estoque"]):
        return jsonify(message="Dados incompletos"), 400

    novo_produto = Produto(
        nome=dados["nome"],
        preco=dados["preco"],
        categoria=dados["categoria"],
        estoque=dados["estoque"],
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify(novo_produto.to_dict()), 201

# Rota para atualizar um produto
@routes.route("/produtos/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_produto(id):
    """Atualiza um produto existente."""
    produto = Produto.query.get_or_404(id)
    dados = request.json

    produto.nome = dados.get("nome", produto.nome)
    produto.preco = dados.get("preco", produto.preco)
    produto.categoria = dados.get("categoria", produto.categoria)
    produto.estoque = dados.get("estoque", produto.estoque)

    db.session.commit()
    return jsonify(produto.to_dict()), 200

# Rota para excluir um produto
@routes.route("/produtos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_produto(id):
    """Exclui um produto."""
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify(message="Produto excluído com sucesso"), 200
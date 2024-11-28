from ext import db

class Produto(db.Model):
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Retorna o objeto como um dicionário."""
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "categoria": self.categoria,
            "estoque": self.estoque,
        }
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# A classe Usuario herda de UserMixin para ter os atributos e métodos que o Flask-Login espera
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256))
    tipo = db.Column(db.String(50), nullable=False, default='turista') # turista, morador, admin

    def set_senha(self, senha):
        """Cria um hash seguro para a senha fornecida."""
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

class PontoTuristico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    localizacao = db.Column(db.String(150))
    categoria = db.Column(db.String(50))
    horario = db.Column(db.String(100))
    preco = db.Column(db.Float)
    imagem_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    # Relacionamento para acessar os eventos a partir de um ponto turístico
    eventos = db.relationship('Evento', backref='ponto', lazy=True)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(50))
    local = db.Column(db.String(150))
    detalhes = db.Column(db.Text)
    imagem_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    # Chave estrangeira que liga o evento a um ponto turístico
    ponto_id = db.Column(db.Integer, db.ForeignKey('ponto_turistico.id'), nullable=False)
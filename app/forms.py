from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais.')])
    tipo = SelectField('Tipo de Usuário', choices=[('turista', 'Turista'), ('morador', 'Morador')])
    submit = SubmitField('Criar Conta')

from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField

# ... (as classes LoginForm e RegisterForm já existem aqui) ...

class PontoTuristicoForm(FlaskForm):
    nome = StringField('Nome do Local', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    localizacao = StringField('Localização (ex: Eixo Monumental)')
    categoria = StringField('Categoria (ex: Monumento, Parque)')
    horario = StringField('Horário de Funcionamento')
    preco = FloatField('Preço do Ingresso (use 0 para gratuito)')
    imagem = FileField('Imagem do Local', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Salvar')

class EventoForm(FlaskForm):
    nome = StringField('Nome do Evento', validators=[DataRequired()])
    data_evento = StringField('Data (ex: DD/MM/AAAA)') # <-- RENOMEADO
    local = StringField('Local do Evento')
    detalhes = TextAreaField('Detalhes do Evento')
    ponto = SelectField('Associado ao Ponto Turístico', coerce=int, validators=[DataRequired()])
    imagem = FileField('Imagem do Evento', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Salvar')
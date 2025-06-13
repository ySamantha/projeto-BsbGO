# Imports que já existiam
import secrets
import os
from werkzeug.utils import secure_filename
from flask import current_app

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import Usuario, PontoTuristico, Evento
from .forms import LoginForm, RegisterForm, PontoTuristicoForm, EventoForm # Adicionamos os novos formulários aqui
from . import db

# Imports novos que adicionamos
from functools import wraps
from flask import abort

def save_picture(form_picture):
    # Gera um nome de arquivo aleatório para evitar conflitos
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Define o caminho completo onde a imagem será salva
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)

    # Cria a pasta de uploads se ela não existir
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Salva a imagem
    form_picture.save(picture_path)

    return picture_fn

main = Blueprint('main', __name__)

# --- ROTAS PÚBLICAS (JÁ EXISTIAM) ---

@main.route('/')
def index():
    pontos = PontoTuristico.query.all()
    eventos = Evento.query.all()
    return render_template('index.html', pontos=pontos, eventos=eventos)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_senha(form.senha.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # --- MUDANÇA AQUI ---
            # Criamos o usuário e definimos os campos um a um
            user = Usuario()
            user.nome = form.nome.data
            user.email = form.email.data
            user.tipo = form.tipo.data
            user.set_senha(form.senha.data)
            # --- FIM DA MUDANÇA ---

            db.session.add(user)
            db.session.commit()
            flash('Conta criada com sucesso! Faça o login.', 'success')
            return redirect(url_for('main.login'))
        
        flash('Este endereço de e-mail já está em uso.', 'warning')

    return render_template('register.html', form=form)


# --- INÍCIO DO CÓDIGO DE ADMIN ---

# DECORATOR PARA PROTEGER ROTAS DE ADMIN
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'admin':
            abort(403) # Proibido o acesso
        return f(*args, **kwargs)
    return decorated_function

# --- ROTAS PARA PONTOS TURÍSTICOS ---

@main.route('/admin/pontos')
@login_required
@admin_required
def admin_pontos():
    pontos = PontoTuristico.query.all()
    return render_template('admin_manager.html', items=pontos, title="Locais Turísticos", item_type="ponto")

@main.route('/admin/ponto/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_ponto():
    form = PontoTuristicoForm()
    if form.validate_on_submit():
        # --- CÓDIGO CORRIGIDO ---
        # Criamos um objeto vazio e depois definimos cada campo
        novo_ponto = PontoTuristico()
        novo_ponto.nome = form.nome.data
        novo_ponto.descricao = form.descricao.data
        novo_ponto.localizacao = form.localizacao.data
        novo_ponto.categoria = form.categoria.data
        novo_ponto.horario = form.horario.data
        novo_ponto.preco = form.preco.data
        
        # A lógica para salvar a imagem continua a mesma
        if form.imagem.data:
            picture_file = save_picture(form.imagem.data)
            novo_ponto.imagem_file = picture_file
        
        db.session.add(novo_ponto)
        db.session.commit()
        flash('Ponto turístico adicionado com sucesso!', 'success')
        return redirect(url_for('main.admin_pontos'))
    return render_template('form_page.html', form=form, title="Adicionar Novo Ponto Turístico")

@main.route('/admin/ponto/editar/<int:ponto_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ponto(ponto_id):
    ponto = PontoTuristico.query.get_or_404(ponto_id)
    form = PontoTuristicoForm(obj=ponto)
    if form.validate_on_submit():
        if form.imagem.data:
            picture_file = save_picture(form.imagem.data)
            ponto.imagem_file = picture_file

        ponto.nome = form.nome.data
        ponto.descricao = form.descricao.data
        ponto.localizacao = form.localizacao.data
        ponto.categoria = form.categoria.data
        ponto.horario = form.horario.data
        ponto.preco = form.preco.data
        db.session.commit()
        flash('Ponto turístico atualizado com sucesso!', 'success')
        return redirect(url_for('main.admin_pontos'))
    return render_template('form_page.html', form=form, title="Editar Ponto Turístico")

@main.route('/admin/ponto/deletar/<int:ponto_id>', methods=['POST'])
@login_required
@admin_required
def deletar_ponto(ponto_id):
    ponto = PontoTuristico.query.get_or_404(ponto_id)
    db.session.delete(ponto)
    db.session.commit()
    flash('Ponto turístico deletado com sucesso!', 'success')
    return redirect(url_for('main.admin_pontos'))

# --- ROTAS PARA EVENTOS ---

@main.route('/admin/eventos')
@login_required
@admin_required
def admin_eventos():
    eventos = Evento.query.all()
    return render_template('admin_manager.html', items=eventos, title="Eventos", item_type="evento")

@main.route('/admin/evento/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_evento():
    form = EventoForm()
    form.ponto.choices = [(p.id, p.nome) for p in PontoTuristico.query.order_by('nome').all()]
    if form.validate_on_submit():
        novo_evento = Evento()
        novo_evento.nome = form.nome.data
        novo_evento.data = form.data_evento.data
        novo_evento.local = form.local.data
        novo_evento.detalhes = form.detalhes.data
        novo_evento.ponto_id = form.ponto.data
        
        if form.imagem.data:
            picture_file = save_picture(form.imagem.data)
            novo_evento.imagem_file = picture_file
        
        db.session.add(novo_evento)
        db.session.commit()
        flash('Evento adicionado com sucesso!', 'success')
        return redirect(url_for('main.admin_eventos'))
    return render_template('form_page.html', form=form, title="Adicionar Novo Evento")

@main.route('/admin/evento/editar/<int:evento_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    # Aqui populamos o formulário. O WTForms é inteligente o suficiente para associar
    # evento.data com o campo form.data_evento, então não precisa mudar aqui.
    form = EventoForm(obj=evento) 
    form.ponto.choices = [(p.id, p.nome) for p in PontoTuristico.query.order_by('nome').all()]
    if form.validate_on_submit():
        
        if form.imagem.data:
            picture_file = save_picture(form.imagem.data)
            evento.imagem_file = picture_file
        
        evento.nome = form.nome.data
        evento.data = form.data_evento.data # <-- MUDANÇA AQUI
        evento.local = form.local.data
        evento.detalhes = form.detalhes.data
        evento.ponto_id = form.ponto.data
        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('main.admin_eventos'))
    
    # populamos o valor do select e do campo de data ao carregar a página
    form.ponto.data = evento.ponto_id
    form.data_evento.data = evento.data # <-- MUDANÇA AQUI
    return render_template('form_page.html', form=form, title="Editar Evento")


@main.route('/admin/evento/deletar/<int:evento_id>', methods=['POST'])
@login_required
@admin_required
def deletar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento deletado com sucesso!', 'success')
    return redirect(url_for('main.admin_eventos'))

# --- FIM DO CÓDIGO DE ADMIN ---
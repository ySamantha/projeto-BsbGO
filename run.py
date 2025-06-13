from app import create_app, db
from app.models import Usuario, PontoTuristico, Evento

# Cria a instância da aplicação usando a factory
app = create_app()

def setup_database(app):
    """Função para criar tabelas e popular dados iniciais."""
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos
        db.create_all()

        # Adiciona um usuário admin se ele não existir
        if not Usuario.query.filter_by(email="admin@bsbgo.com").first():
            admin = Usuario(nome="Admin", email="admin@bsbgo.com", tipo="admin")
            admin.set_senha("admin123")
            db.session.add(admin)

        # Adiciona um ponto turístico de exemplo se não houver nenhum
        if not PontoTuristico.query.first():
            pt1 = PontoTuristico(
                nome="Catedral Metropolitana de Brasília",
                descricao="Um marco da arquitetura moderna projetado por Oscar Niemeyer.",
                localizacao="Eixo Monumental",
                categoria="Monumento",
                horario="08:00 - 17:00",
                preco=0.0
            )
            pt2 = PontoTuristico(
                nome="Parque Nacional de Brasília (Água Mineral)",
                descricao="Conhecido por suas piscinas de água mineral e trilhas ecológicas.",
                localizacao="Via Epia",
                categoria="Parque",
                horario="08:00 - 16:00",
                preco=16.0
            )
            db.session.add(pt1)
            db.session.add(pt2)
        
        # Adiciona um evento de exemplo se não houver nenhum
        if not Evento.query.first():
            ev = Evento(
                nome="Show da Banda Natiruts",
                data="30/08/2025",
                local="Arena BRB Mané Garrincha",
                detalhes="Show da turnê de despedida da banda.",
                ponto_id=1 # Associa ao primeiro ponto turístico criado
            )
            db.session.add(ev)

        # Salva todas as mudanças no banco de dados
        db.session.commit()
        print("Banco de dados configurado com dados iniciais.")

# O bloco abaixo só é executado quando o script é chamado diretamente (python run.py)
if __name__ == '__main__':
    # Chama a função para configurar o banco de dados
    setup_database(app)
    # Inicia o servidor de desenvolvimento do Flask
    app.run(debug=True)
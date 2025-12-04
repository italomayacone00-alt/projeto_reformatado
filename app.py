from dotenv import load_dotenv
# ==========================================================
# 1. Carrega as variáveis do arquivo .env (deve estar na raiz do projeto)
# ==========================================================
load_dotenv() 

from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
# Importação do Blueprint (que agora não gera mais o ciclo)
from controllers.product_controller import products_bp
# NOVO: Importa 'db' do seu novo arquivo de extensão
from db import db 


# Cria e configura a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# ==========================================================
# 2. Inicializa o banco de dados com o objeto 'app'
# ==========================================================
db.init_app(app) 

# Configura o local das views (templates)
app.template_folder = 'views/templates'
app.static_folder = 'static'

# Registra o Blueprint do Produto
app.register_blueprint(products_bp, url_prefix='/products')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        if user == 'admin' and password == '1234':
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main_page'))
        else:
            error = "Usuário ou senha incorretos!"
    return render_template('login.html', error=error)

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/vendas')
def vendas():
    return render_template('vendas/index.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos/index.html')

@app.route('/estoque')
def estoque():
    return render_template('estoque/index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes/index.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios/index.html')

@app.route('/qualidade')
def qualidade():
    return render_template('qualidade/index.html')

# Rota de tratamento de erro 404 (Opcional)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ==========================================================
# 3. Criação das tabelas (com o contexto da aplicação)
# Deve ser executado ANTES de rodar o app para criar as tabelas
# no Supabase/SQLite.
# ==========================================================
with app.app_context():
    # Cria todas as tabelas definidas nos seus modelos (Product)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
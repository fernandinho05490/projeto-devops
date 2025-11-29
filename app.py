from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do Banco de Dados (Pega do Docker ou usa padrão)
# Isso satisfaz o requisito de "armazenar em base de dados"
db_user = os.environ.get('POSTGRES_USER', 'user')
db_password = os.environ.get('POSTGRES_PASSWORD', 'password')
db_name = os.environ.get('POSTGRES_DB', 'todo_db')
db_host = os.environ.get('DB_HOST', 'db') # 'db' é o nome do serviço no Docker

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela (O que vamos salvar)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()

# Rota para o Front-end
@app.route('/')
def index():
    return render_template('index.html')

# Rota GET (Listar tarefas) - Requisito JSON
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title}
        output.append(task_data)
    return jsonify({'tasks': output})

# Rota POST (Criar tarefa) - Requisito JSON e POST
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tarefa criada!'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
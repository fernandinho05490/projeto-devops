from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do Banco de Dados
db_user = os.environ.get('POSTGRES_USER', 'user')
db_password = os.environ.get('POSTGRES_PASSWORD', 'password')
db_name = os.environ.get('POSTGRES_DB', 'todo_db')
db_host = os.environ.get('DB_HOST', 'db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela (Atualizado com status)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)  # Nova coluna!

# Cria as tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Rota GET (Listar)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.id).all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'done': task.done}
        output.append(task_data)
    return jsonify({'tasks': output})

# Rota POST (Criar)
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tarefa criada!'}), 201

# Rota PUT (Atualizar Status) - NOVO
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    
    task.done = not task.done  # Inverte o status (se era False vira True)
    db.session.commit()
    return jsonify({'message': 'Status atualizado!'})

# Rota DELETE (Apagar) - NOVO
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarefa deletada!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
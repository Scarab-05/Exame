from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'a_sua_chave_secreta'  # Chave secreta para a aplicação
app.config['SESSION_TYPE'] = 'filesystem'  # Persistir sessões no sistema de arquivos
Session(app)

# Placeholder para a base de dados
rooms = [
    {"id": 1, "name": "A458", "capacity": 10},
    {"id": 2, "name": "B436", "capacity": 20},
    {"id": 3, "name": "C157", "capacity": 15},
    {"id": 4, "name": "D549", "capacity": 25},
    {"id": 5, "name": "E768", "capacity": 30}
]

# Adicionar reservas de exemplo
reservations = [
    {"room_id": 1, "start_time": "2026-02-05T09:00:00", "end_time": "2026-02-05T10:00:00", "email": "user1@example.com", "name": "Utilizador 1"},
    {"room_id": 2, "start_time": "2026-02-05T11:00:00", "end_time": "2026-02-05T12:00:00", "email": "user2@example.com", "name": "Utilizador 2"},
    {"room_id": 3, "start_time": "2026-02-06T14:00:00", "end_time": "2026-02-06T15:00:00", "email": "user3@example.com", "name": "Utilizador 3"},
    {"room_id": 4, "start_time": "2026-02-07T10:00:00", "end_time": "2026-02-07T11:30:00", "email": "user4@example.com", "name": "Utilizador 4"},
    {"room_id": 5, "start_time": "2026-02-08T13:00:00", "end_time": "2026-02-08T14:30:00", "email": "user5@example.com", "name": "Utilizador 5"}
]

users = []  # Lista para armazenar utilizadores registados

# Credenciais do administrador
ADMIN_CREDENTIALS = {
    "username": "ADMIN",
    "password": "ADMIN123"
}

@app.route('/')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', rooms=rooms)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        # Verificar se o email está registado
        if any(user['email'] == email for user in users):
            session['email'] = email
            return redirect(url_for('home'))
        return render_template('login.html', error="Email não registado. Por favor, registe-se primeiro.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        if email and name:
            users.append({"email": email, "name": name})
            session['email'] = email
            return redirect(url_for('home'))
        return render_template('register.html', error="Por favor, preencha todos os campos.")
    return render_template('register.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template('admin_login.html', error="Credenciais inválidas.")
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/reservations', methods=['GET'])
def get_reservations():
    if 'email' not in session:
        return redirect(url_for('login'))
    return jsonify(reservations)

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    user_email = session.get('email')  # Buscar email do utilizador na sessão
    user_name = next((user['name'] for user in users if user['email'] == user_email), None)  # Buscar nome do utilizador registado

    if not user_email or not user_name:
        return jsonify({'error': 'Usuário não autenticado.'}), 401

    room_id = data.get('room_id')
    start_time = datetime.fromisoformat(data.get('start_time')).replace(tzinfo=None)  # Garantir que o horário não tenha fuso horário
    end_time = datetime.fromisoformat(data.get('end_time')).replace(tzinfo=None)  # Garantir que o horário não tenha fuso horário

    # Verificar se o horário já passou
    if start_time < datetime.now():
        return jsonify({"error": "Não é possível reservar uma sala para um horário que já passou."}), 400

    # Verificar sobreposição de reservas
    for res in reservations:
        existing_start = datetime.fromisoformat(res['start_time']).replace(tzinfo=None)
        existing_end = datetime.fromisoformat(res['end_time']).replace(tzinfo=None)
        if res['room_id'] == room_id and not (existing_end <= start_time or existing_start >= end_time):
            return jsonify({"error": "A sala já está reservada para o horário selecionado."}), 400

    # Adicionar reserva
    reservations.append({
        "room_id": room_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "email": user_email,
        "name": user_name
    })
    return jsonify({"message": "Reserva efetuada com sucesso."})

@app.route('/cancel', methods=['POST'])
def cancel_reservation():
    if 'email' not in session:
        return jsonify({"error": "Usuário não autenticado."}), 401

    data = request.json
    email = session['email']
    room_id = data['room_id']
    start_time = data['start_time']
    end_time = data['end_time']

    # Verificar se a reserva existe e se pertence ao utilizador
    for res in reservations:
        if res['email'] == email and res['room_id'] == room_id and res['start_time'] == start_time and res['end_time'] == end_time:
            reservations.remove(res)
            return jsonify({"message": "Reserva cancelada com sucesso."})

    return jsonify({"error": "Reserva não encontrada ou não pertence ao utilizador."}), 404

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin.html', rooms=rooms, reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
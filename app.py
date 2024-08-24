from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from src.game.game_manager import Game
from src.administration.user_manager import User, UserManager
from src.administration.fill_base import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Creating a UserManager object
user_manager = UserManager()

# Example of user role verification (suppose 2 is an administrator)
def is_admin():
    return session.get('role_id') == 2

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('game'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nick_or_email = request.form['nick_or_email']
        password = request.form['password']

        # User authorization via UserManager
        success, result = user_manager.authenticate(nick_or_email, password)

        if success:
            user = result
            session['user_id'] = user.user_id
            session['username'] = user.nick
            session['name'] = user.name
            session['role_id'] = user.role_id
            flash('Login successful!', 'success')
            return redirect(url_for('game'))
        else:
            flash(result, 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nick = request.form['nick']
        email = request.form['email']
        name = request.form['name']
        birthdate = request.form['birthdate']
        password = request.form['password']

        # User registration via UserManager
        success, message = user_manager.register(nick, email, name, birthdate, password)

        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not is_admin():
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'fill_genres' in request.form:
            fill_genres()
            flash('Genres filled successfully.', 'success')
        elif 'fill_films' in request.form:
            fill_films()
            flash('Films filled successfully.', 'success')
        elif 'fill_people' in request.form:
            fill_people()
            flash('People filled successfully.', 'success')
        elif 'fill_keywords' in request.form:
            fill_keywords()
            flash('Keywords filled successfully.', 'success')
        elif 'fill_all_data' in request.form:
            page = int(request.form['page'])
            fill_all_data_films_by_page(page)
            flash(f'Data for page {page} filled successfully.', 'success')

    return render_template('admin.html')

@app.route('/fill_all_data', methods=['POST'])
def fill_all_data():
    if not is_admin():
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))

    page = int(request.form.get('page'))
    fill_all_data_films_by_page(page)
    flash(f'All data for page {page} filled successfully.', 'success')
    return redirect(url_for('admin'))

@app.route('/game')
def game():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access the game.', 'danger')
        return redirect(url_for('login'))

    # Создаем объект Game для текущего пользователя
    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    game = Game(user)
    
    # Сохраняем минимальные данные в сессии, такие как id фильма
    session['film_id'] = game.film[0]  # Предполагается, что film[0] — это идентификатор фильма
    
    # Получаем первую подсказку
    first_hint = game.get_keywordsHint()
    session['current_hint_index'] = 1  # Устанавливаем текущий индекс подсказки

    hints = {'keywords': first_hint}  # Создаем словарь с первой подсказкой

    return render_template('index.html', hints=hints, game_started=True)


@app.route('/start_game', methods=['POST'])
def start_game():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to start the game.', 'danger')
        return redirect(url_for('login'))

    # Создаем игру для текущего пользователя
    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    game = Game(user)
    session['film_id'] = game.film[0]  # Предполагается, что film[0] — это идентификатор фильма
    session['current_hint_index'] = 1  # Сохраняем текущий индекс подсказки

    first_hint = game.get_keywordsHint()
    hints = {'keywords': first_hint}

    return jsonify({'game_started': True, 'hints': hints})


@app.route('/get_hint', methods=['POST'])
def get_hint():
    if 'username' not in session or 'user_id' not in session:
        return jsonify({'hint': None}), 403

    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    film_id = session.get('film_id')
    if not film_id:
        return jsonify({'hint': None}), 404

    game = Game(user)
    game.film = (film_id,) + game.film[1:]  # Восстановление фильма

    current_index = session.get('current_hint_index', 1)
    hint = None

    if current_index == 1:
        hint = game.get_keywordsHint()
    elif current_index == 2:
        hint = game.get_genreHint()
    elif current_index == 3:
        hint = game.get_actorsHint()
    elif current_index == 4:
        hint = game.get_yearHint()
    elif current_index == 5:
        hint = game.get_descriptionHint()
    elif current_index == 6:
        hint = game.get_imageHint()

    if hint:
        session['current_hint_index'] = current_index + 1
        return jsonify({'hint': hint})
    else:
        return jsonify({'hint': None}), 404


@app.route('/check_answer', methods=['POST'])
def check_answer():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to check the answer.', 'danger')
        return redirect(url_for('login'))

    user_answer = request.form['answer'].strip().lower()
    
    film_id = session.get('film_id')
    if not film_id:
        return jsonify({'result': 'No game in progress.', 'correct': False}), 404

    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    game = Game(user)
    game.film = (film_id,) + game.film[1:]  # Восстановление фильма

    # Отладочный вывод для проверки содержимого game.film
    print(f"Debug: game.film = {game.film}")
    
    # Правильный индекс для названия фильма — game.film[5]
    correct_answer = game.film[5].strip().lower()

    if user_answer == correct_answer:
        return jsonify({'result': 'Correct!', 'correct': True})
    else:
        return jsonify({'result': 'Incorrect. Try again!', 'correct': False})




if __name__ == '__main__':
    app.run(debug=True)

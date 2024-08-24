from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

from src.game.game_manager import Game
from src.administration.user_manager import User, UserManager
from src.administration.fill_base import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()

# Function to check if the current user is an admin
def is_admin():
    return session.get('role_id') == 2

# Save the game object to the session
def save_game_to_session(game):
    session['game'] = pickle.dumps(game)

# Load the game object from the session
def load_game_from_session():
    game_data = session.get('game')
    return pickle.loads(game_data) if game_data else None

@app.route('/')
def home():
    return redirect(url_for('game') if 'username' in session else 'login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nick_or_email = request.form['nick_or_email']
        password = request.form['password']

        # User authentication via UserManager
        success, result = user_manager.authenticate(nick_or_email, password)

        if success:
            user = result
            session['user_id'] = user.user_id
            session['username'] = user.nick
            session['name'] = user.name
            session['role_id'] = user.role_id
            
            flash('Login successful!', 'success')
            
            # Redirect to admin page if the user is an admin
            if user.role_id == 2:  # Assuming role_id 2 is for administrators
                return redirect(url_for('admin'))
            else:
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
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    if not is_admin():
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        actions = {
            'fill_genres': fill_genres,
            'fill_films': fill_films,
            'fill_people': fill_people,
            'fill_keywords': fill_keywords,
            'fill_all_data': lambda: fill_all_data_films_by_page(int(request.form['page']))
        }

        for action, func in actions.items():
            if action in request.form:
                func()
                flash(f'{action.replace("_", " ").title()} completed successfully.', 'success')

    return render_template('admin.html')

@app.route('/fill_all_data', methods=['POST'])
def fill_all_data():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

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
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('role_id') == 2:
        return redirect(url_for('admin'))

    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    game = Game(user)
    save_game_to_session(game)

    first_hint = game.get_keywordsHint()
    session['current_hint_index'] = 1

    hints = {'keywords': first_hint}

    return render_template('index.html', hints=hints, game_started=True)

@app.route('/start_game', methods=['POST'])
def start_game():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    user = User(session['user_id'], session['username'], session['name'], session['role_id'])
    game = Game(user)
    save_game_to_session(game)

    first_hint = game.get_keywordsHint()
    session['current_hint_index'] = 1

    hints = {'keywords': first_hint}

    return jsonify({'game_started': True, 'hints': hints})

@app.route('/get_hint', methods=['POST'])
def get_hint():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    game = load_game_from_session()

    hint_funcs = {
        1: game.get_genreHint,
        2: game.get_actorsHint,
        3: game.get_yearHint,
        4: game.get_descriptionHint,
        5: game.get_imageHint
    }

    current_index = session.get('current_hint_index', 1)
    hint = hint_funcs.get(current_index, lambda: None)()

    if hint:
        session['current_hint_index'] = current_index + 1
        return jsonify({'hint': hint})
    else:
        return jsonify({'hint': None}), 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    user_answer = request.form['answer'].strip().lower()
    game = load_game_from_session()

    correct_answer = game.film[5].strip().lower()
    is_correct = user_answer == correct_answer

    return jsonify({'result': 'Correct!' if is_correct else 'Incorrect. Try again!', 'correct': is_correct})

@app.route('/end_game', methods=['POST'])
def end_game():
    if 'username' not in session or 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    session.pop('game', None)  # Remove the current game from the session
    session.pop('film_id', None)  # Remove the current film from the session
    session.pop('current_hint_index', None)  # Remove the current hint index from the session
    return jsonify({'status': 'Game ended'})

if __name__ == '__main__':
    app.run(debug=True)

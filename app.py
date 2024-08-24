from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from src.administration.user_manager import UserManager
from src.administration.fill_base import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Creating a UserManager object
user_manager = UserManager()

# Example of user role verification (suppose 2 is an administrator)
def is_admin():
    return 'role_id' in session and session['role_id'] == 2

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

        # # User authorization via User Manager
        success, result = user_manager.authenticate(nick_or_email, password)

        if success:
            user = result
            session['username'] = user[1]  # user[1] - this is nick
            session['role_id'] = user[5]  # user[5] - this is role_id
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
    session.pop('username', None)
    session.pop('role_id', None)
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

# @app.route('/game')
# def game():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     hints = {
#         'keywords': 'jkljjbjhvkjh',
#         'year': 'hshsj;kj;j;',
#         'actors': 'kjnlkjn;',
#         'image': 'ohgosjgshjoj',
#         'description': 'hlahlghakljghalkhl'
#     }

#     return render_template('index.html', hints=hints)

@app.route('/start_game', methods=['POST'])
def start_game():
@app.route('/start_game', methods=['POST'])
def start_game():
    # Здесь вы должны сгенерировать или выбрать фильм для игры
    movie = get_random_movie()  # Предположим, у вас есть функция, выбирающая случайный фильм
    hints = {
        'keywords': KeywordsHint().get_hint(movie),
        'year': YearHint().get_hint(movie),
        'actors': ActorsHint().get_hint(movie),
        'image': ImageHint().get_hint(movie),
        'description': DescriptionHint().get_hint(movie)
    }
    session['movie_id'] = movie.id  # Сохраняем идентификатор фильма в сессии
    session['hints'] = hints  # Сохраняем подсказки в сессии
    return render_template('index.html', hints=hints, game_started=True)



if __name__ == '__main__':
    app.run(debug=True)

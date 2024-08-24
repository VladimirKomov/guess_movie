from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from src.administration.user_manager import UserManager
# from src.administration.api_manager import ApiManager
# from src.administration.primary_filling_manager import PrimaryFillingManager
from src.administration.fill_base import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Создание объекта UserManager
user_manager = UserManager()

# Пример проверки роли пользователя (предположим, 2 - администратор)
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

        # Авторизация пользователя через UserManager
        user = user_manager.authenticate_user(nick_or_email, password)

        if user:
            session['username'] = user[1]  # user[1] - это поле nick
            session['role_id'] = user[5]  # user[5] - это поле role_id
            flash('Login successful!', 'success')
            return redirect(url_for('game'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nick = request.form['nick']
        email = request.form['email']
        name = request.form['name']
        birthdate = request.form['birthdate']
        # role_id = request.form['role_id']  # Ожидается выбор роли (например, 1 - пользователь, 2 - администратор)
        password = request.form['password']

        # Проверка существования пользователя через UserManager
        if not user_manager.user_exists(nick, email):
            success = user_manager.register_user(
                nick=nick,
                email=email,
                name=name,
                birthdate=birthdate,
                # role_id=role_id,
                password=password
            )
            if success:
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Please try again.', 'danger')
        else:
            flash('Username or email already exists. Please choose another one.', 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/game')
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    hints = {
        'keywords': 'jkljjbjhvkjh',
        'year': 'hshsj;kj;j;',
        'actors': 'kjnlkjn;',
        'image': 'ohgosjgshjoj',
        'description': 'hlahlghakljghalkhl'
    }

    return render_template('index.html', hints=hints)

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

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

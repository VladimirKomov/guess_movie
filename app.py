from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from src.administration.user_manager import UserManager


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Создание объекта подключения к базе данных
# db_connection = DatabaseConnection()
# Создание объекта UserManager
user_manager = UserManager()

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
        role = request.form['role']
        password = request.form['password']

        # Проверка существования пользователя через UserManager
        if not user_manager.user_exists(nick, email):
            success = user_manager.register_user(
                nick=nick,
                email=email,
                name=name,
                birthdate=birthdate,
                role=role,
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
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/game')
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer'].lower()
    correct_answer = "the shawshank redemption"  # Пример правильного ответа
    result = "Correct!" if user_answer == correct_answer else "Incorrect. Try again!"
    return {"result": result}

if __name__ == '__main__':
    app.run(debug=True)

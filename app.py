import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Используй надежный ключ

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Перенаправление на страницу логина

# Простая база пользователей (можно заменить на БД)
users = {"alfeikaa": {"password": "alfeikaa"}}

# Класс пользователя
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

# Форма логина
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неправильные имя или пароль', 'danger')
    return render_template('login.html', form=form)

# Личный кабинет (доступен только авторизованным)
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.id)

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Страница "OK"
@app.route('/ok')
def ok():
    return render_template('ok.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask, render_template, request, g, flash, abort, make_response, redirect, url_for
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin

# configuration
DATABASE = '/tmp/app_db.db'
DEBUG = True
SECRET_KEY = 'bjh?t5-64vyu^&vyYB3dcY0mPYe'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app_db.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print('load-user')
    return UserLogin().from_db(user_id, database)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Допоміжна функція для створення таблиць БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Connecting to the DB, if it is not established yet"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


database = None


@app.before_request
def before_request():
    """Встановлення з'єднання з БД перед виконанням запиту"""
    global database
    db = get_db()
    database = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Closing the connection with DB, if it was established"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():

    # content = render_template('index.html', menu=database.get_menu(), posts=database.get_posts())
    # res = make_response(content)
    # res.headers['Content-Type'] = 'text/plain'
    # res.headers['Server'] = 'flask-zero-23'
    # return res

    # img = None
    # with app.open_resource(app.root_path + '/static/images/IMG-d4580.png',mode='rb') as f:
    #     img = f.read()
    # if img is None:
    #     return 'None image'
    # res = make_response(img)
    # res.headers['Content-Type'] = 'image/png'
    # return res

    # res = make_response('<h1>Помилка сервера</h1>', 500)
    # return res

    # return '<h1>Main Page</h1>', 200, {'Content-Type': 'text/plain'}

    return render_template('index.html', menu=database.get_menu(), posts=database.get_posts())


@app.route('/add-post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['text']) > 10:
            res = database.add_post(request.form['title'], request.form['text'], request.form['url'])
            if not res:
                flash('Помилка при додаванні статті!', category='error')
            else:
                flash('Стаття додана успішно.', category='success')
        else:
            flash('Помилка при додаванні статті!', category='error')

    return render_template('add_post.html', menu=database.get_menu(), title='Додавання статті')


@app.route('/post/<alias>')
def show_post(alias):
    title, text = database.get_post(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=database.get_menu(), title=title, text=text)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = database.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('profile'))

        flash('невірна пара логін/пароль', 'error')

    return render_template('login.html', menu=database.get_menu(), title='Авторизація')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['username']) >= 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash_psw = generate_password_hash(request.form['psw'])
            res = database.add_user(request.form['username'], request.form['email'], hash_psw)
            if res:
                flash('Ви успішно зареєстровані.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Помилка при реєстрації, а саме при додаванні в БД.', 'error')
        else:
            flash('Невірно заповнені поля!', 'error')

    return render_template('register.html', menu=database.get_menu(), title='Реєстрація')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з профілю.', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    print(current_user.get_id())
    return f"""<p><a href="{url_for('logout')}">Log out</a></p><p>user info: {current_user.get_id()}</p>"""


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Page not found - our template'), 404
    # return 'Сторінка не знайдена!', 404


# @app.before_first_request
# def before_first_request():
#     print('before_first_request() called')


# @app.after_request
# def after_request(response):
#     print('after_request() called')
#     return response


# @app.teardown_request
# def teardown_request(response):
#     print('teardown_request() called')
#     return response


if __name__ == '__main__':
    app.run(debug=True)

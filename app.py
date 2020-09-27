from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, make_response
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bcr54t5yvjy45vtg879be45vvh'
app.permanent_session_lifetime = datetime.timedelta(days=10)

menu = [{'name': 'Home', 'url': 'index'},
        {'name': 'Services', 'url': 'services'},
        {'name': 'About us', 'url': 'about'},
        {'name': 'Contact', 'url': 'contact'}]


@app.route('/index')
@app.route('/')
def index():
    print(url_for('index'))
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # Оновлення даних сесії
    else:
        session['visits'] = 1  # Запис данних в сесію
    return f'<h1>Main Page</h1><p>Кількість переглядів: {session["visits"]}</p>'
    # return render_template('index.html', menu=menu)


data = [1, 2, 3, 4]


@app.route('/session')
def session_data():
    session.permanent = False

    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True

    return f'<p>session["data"]: {session["data"]}'


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='Про нас', menu=menu)


@app.route('/some-link/<string:username>/<path:rest>')
def some_link(username, rest):
    # print(url_for('some_link'))
    return f"User: {username}, {rest}"


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Your message sent.', category='success')
        else:
            flash('Some error!', category='error')

        print(request.form)
        print(request.form['username'])

    return render_template('contact.html', title='Feedback', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Page not found', menu=menu), 404


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return render_template('profile.html', title='My profile', menu=menu, username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """SESSION"""
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST' and request.form['username'] == 'qwerty' and request.form['psw'] == '123':
    #     session['userLogged'] = request.form['username']
    #     return redirect(url_for('profile', username=session['userLogged']))
    #
    # return render_template('login_first.html', title='Authorization', menu=menu)

    """COOKIES"""
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f'<h1>Форма авторизації</h1><p>logged: {log}</p>')
    res.set_cookie('logged', 'yes', 24 * 60 * 60)
    return res


@app.route('/logout')
def logout():
    res = make_response('<p>Ви більше не авторизовані!</p>')
    res.set_cookie('logged', '', 0)
    return res


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


if __name__ == '__main__':
    app.run(debug=True)

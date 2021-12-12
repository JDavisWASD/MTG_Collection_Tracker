from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        session.pop('user_id')
    session['error_redirect'] = '/'
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_new_user(request.form):
        return redirect('/registration')

    data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.save(data)
    return redirect('/collection')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/attempt_login', methods = ['POST'])
def attempt_login():
    user = User.get_by_username(request.form['username'])
    if user and \
            bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = user.id
        return redirect('/collection')

    flash('Incorrect username or password.')
    return redirect('/login')

#TODO: Might need to fix back button after logout
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
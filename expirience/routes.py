"""
Runns app and routes
"""

from flask import render_template, url_for, flash, redirect
from .home.log_in import RegisterForm, LoginForm

from expirience import app, db, bcrypt
from .data_base import User, Skills, Projects


@app.route('/')
@app.route('/home')
def home():
    """
    renders home page
    """
    return render_template('home.html', title="Home")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    renders register page
    """
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, country=form.country.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login')
def login():
    """
    renders login page
    """
    form = LoginForm()
    return render_template('login.html', title="Login" , form=form)

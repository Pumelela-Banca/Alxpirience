"""
Runns app and routes
"""

from flask import Flask, render_template, url_for, flash, redirect
from home.log_in import RegisterForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Path: Alxpirience/routes/app.py


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



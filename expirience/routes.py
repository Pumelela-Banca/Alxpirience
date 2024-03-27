"""
Runns app and routes
"""

from flask import render_template, url_for, flash, redirect
from .home.log_in import RegisterForm, LoginForm, UserUpdateForm, CreateJobForm
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
    renders login page and hadles validation
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login Successful', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login" , form=form)


@app.route('/logout')
def logout():
    """
    logs out user
    """
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    """
    renders profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('profile.html', title="Profile")

@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    """
    renders edit profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = UserUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))

@app.route('/addskills', methods=['GET', 'POST'])
def addskills():
    """
    renders add skills page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    

@app.route('/jobs')
def jobs():
    """
    renders jobs page
    all other peoples jobs skips user
    """
    # to do
    return render_template('jobs.html', title="Jobs")


@app.route('/projects')
def projects():
    """
    route to all projects page
    """
    pass

@app.route('/myprojects', methods=['GET', 'POST'])
def myprojects():
    """
    route to user projects page that can be edited
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    pass

@app.route('/createproject', methods=['GET', 'POST'])
def createproject():
    """
    route to create project page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = CreateJobForm()
    if form.validate_on_submit():
        project = Projects(project_name=form.project_name.data, project_description=form.project_description.data, project_link=form.project_link.data)
        db.session.add(project)
        db.session.commit()
        flash(f'Project created for {form.project_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('createproject.html', title="Create Project", form=form)

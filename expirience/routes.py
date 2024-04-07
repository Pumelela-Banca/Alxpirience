"""
Runns app and routes
"""
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from .home.log_in import (RegisterForm, SkillsForm,
                          LoginForm, UserUpdateForm, CreateJobForm)
from flask_login import login_user, current_user, logout_user, login_required

from expirience import app, db, bcrypt
from .data_base import User, Skills, Projects
from expirience.send_email import send_to_job_taker, send_to_job_poster


user_id = None

@app.route('/')
@app.route('/home')
def home():
    """
    renders home page
    """
    jobs = Projects.query.all()
    return render_template('home.html', title="Home", jobs=jobs)

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
        user = User(username=form.username.data,
                    email=form.email.data,
                    country=form.country.data,
                    git_hub=form.git_hub.data,
                    password=hashed_password,
                    image_file=url_for('static', filename='profile_pics/' + 'Generic-Profile-Image.png'))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
@login_required
def profile():
    """
    renders profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    image_file = current_user.image_file
    if not Skills.query.all():
        return render_template('profile.html', title="Profile", form=None)
    return render_template('profile.html', title="Profile", image_file=image_file,
                           form=Skills.query.filter_by(author=current_user).all())

def save_picture(form_picture):
    """
    saves picture to file
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize picture for memory
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    """
    renders edit profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = UserUpdateForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    return render_template('editprofile.html', image_file=image_file,
                           title="Edit Profile", form=form)

@app.route('/addskills', methods=['GET', 'POST'])
@login_required
def addskills():
    """
    renders add skills page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SkillsForm()
    if form.validate_on_submit():
        for value in form.data.values():
            if value == 'Submit' or value == None:
                continue
            skill = Skills(skill=value, author=current_user)
            db.session.add(skill)
            db.session.commit()
        flash('Skills added!', 'success')
        return redirect(url_for('home'))
    return render_template('addskills.html', title="Add Skills", form=form)

@app.route('/projects')
def projects():
    """
    route to all projects page
    """
    render_template('projects.html', title="Projects")

@app.route('/myprojects', methods=['GET', 'POST'])
@login_required
def myprojects():
    """
    route to user projects page that can be edited
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        project_id = request.form.get('item_id')
        project = Projects.query.get(project_id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted!', 'success')
        return redirect(url_for('myprojects'))
    projects_current_user = [Projects.query.all(), current_user]
    return render_template('myprojects.html', title="My Projects", form=projects_current_user)

@app.route('/createproject', methods=['GET', 'POST'])
@login_required
def createproject():
    """
    route to create project page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CreateJobForm()
    if form.validate_on_submit():

        project = Projects(project_name=form.job_title.data,
                           project_description=form.job_description.data,
                           project_link=form.job_link.data,
                           skills_required=form.skills_required.data,
                           author=current_user)
        db.session.add(project)
        db.session.commit()
        flash(f'Project created for {form.job_title.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('createproject.html', title="Create Project", form=form)


@app.route('/about')
def about():
    """
    renders about page
    """
    return render_template('about.html', title="About")

@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def get_job():
    """
    route to get job page and apply for job
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        project_id = request.form.get('item_id')
        #project = Projects.query.get(project_id)
        send_to_job_taker(current_user.id, project_id)
        send_to_job_poster(current_user.id, project_id)
        flash('Accepted Job - Email sent', 'success')
        return redirect(url_for('home'))
    projects_current_user = [Projects.query.all(), current_user]
    return render_template('jobs.html', title="Get Job", form=projects_current_user)

"""
User funtionality rooutes
"""
from mailersend import emails
from .forms import (RegisterForm, ResetPasswordForm, RequestResetForm,
                          LoginForm, UserUpdateForm)
from flask_login import login_user, current_user, logout_user, login_required

from .. import db, bcrypt
from ..data_base import User, Projects, Skills
from .utils import save_picture, send_reset_email


key = open("expirience/access_token.txt", "r").read().rstrip("\n")

mailer = emails.NewEmail(key)

user_id = None

from flask import Blueprint, render_template, redirect, url_for, flash, request


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    renders register page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    country=form.country.data,
                    git_hub=form.git_hub.data,
                    password=hashed_password,
                    image_file='Generic-Profile-Image.png')
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    renders login page and hadles validation
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login Successful', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login" , form=form)


@users.route('/logout')
def logout():
    """
    logs out user
    """
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    """
    renders edit profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
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
        return redirect(url_for('users.profile'))
    return render_template('editprofile.html', image_file=image_file,
                           title="Edit Profile", form=form)

@users.route('/myprojects', methods=['GET', 'POST'])
@login_required
def myprojects():
    """
    route to user projects page that can be edited
    """
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        project_id = request.form.get('item_id')
        project = Projects.query.get(project_id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted!', 'success')
        return redirect(url_for('users.myprojects'))
    projects_current_user = [Projects.query.all(), current_user]
    return render_template('myprojects.html', title="My Projects", form=projects_current_user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """
    resets password
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Takes in reset token
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route('/user/<string:username>', methods=['GET', 'POST'])
def user_jobs(username):
    """
    gets user specific jobs
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Projects.query.filter_by(author=user)\
        .paginate(page=page, per_page=5)
    return render_template('user_jobs.html',
                           title="Home", jobs=jobs, user=user)

@users.route('/profile')
@login_required
def profile():
    """
    renders profile page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    image_file = image_file = url_for('static',
                                      filename='profile_pics/' + \
                                        current_user.image_file)
    if not Skills.query.all():
        return render_template('profile.html', title="Profile", form=None)
    return render_template('profile.html', title="Profile", image_file=image_file,
                           form=Skills.query.filter_by(author=current_user).all())

"""
Project routes or Jobs
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..data_base import Projects, User
from .utils import send_to_job_taker, send_to_job_poster
from .. import db
from flask_login import current_user, login_required
from .forms import CreateJobForm

jobs = Blueprint('jobs', __name__)


@jobs.route('/projects')
def projects():
    """
    route to all projects page
    """
    render_template('projects.html', title="Projects")


@jobs.route('/user/<string:username>', methods=['GET', 'POST'])
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

@jobs.route('/myprojects', methods=['GET', 'POST'])
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

@jobs.route('/createproject', methods=['GET', 'POST'])
@login_required
def createproject():
    """
    route to create project page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('main.home'))
    return render_template('createproject.html', title="Create Project", form=form)

@jobs.route('/jobs', methods=['GET', 'POST'])
@login_required
def get_job():
    """
    route to get job page and jobsly for job
    """
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        project_id = request.form.get('item_id')
        #project = Projects.query.get(project_id)
        send_to_job_taker(current_user.id, project_id)
        send_to_job_poster(current_user.id, project_id)
        flash('Accepted Job - Email sent', 'success')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    projects_current_user = [Projects.query.paginate(page=page, per_page=5), current_user]
    return render_template('jobs.html', title="Get Job", form=projects_current_user)

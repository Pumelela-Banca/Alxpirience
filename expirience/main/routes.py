"""
Runns main and routes
"""
from flask import Blueprint, request
from flask import render_template
from ..data_base import Projects

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """
    renders home page
    """
    page = request.args.get('page', 1, type=int)
    jobs = Projects.query.paginate(page=page, per_page=5)
    return render_template('home.html', title="Home", jobs=jobs)


@main.route('/about')
def about():
    """
    renders about page
    """
    return render_template('about.html', title="About")

"""
Tests account items after log in
"""
from expirience.data_base import User, Projects, Skills
import bcrypt


form_data = {
    'username': 'testuser',
    'email'   : 'bob@gmail.com',
    'password': 'secret--1',
    'git_hub': 'Git-Bob',
    'country' : 'Algeria',
    'confirm_password': 'secret--1',
}

def test_registration(client, app):
    """
    test registartion functionality
    """
    
    response = client.post("/register", data=form_data)
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        print(User.query.all())
        assert response.status_code == 200
        assert user.email == 'bob@gmail.com'
        assert user.git_hub == 'Git-Bob'
        assert user.country == 'Algeria'
        assert bcrypt.checkpw(
            form_data['confirm_password'].encode('utf-8'),
            user.password.encode('utf-8')
        )


def test_login(client, app):
    """
    test login functionality
    """
    login_form = {
        'username': 'testuser',
        'password': 'secret--1'
    }
    response = client.post("/login", data=login_form)
    assert response.status_code == 200
    assert b"<title>Home Page</title>" in response.data
    

def test_projects(client, app):
    """
    test projects functionality
    """
    project_form = {
        'project_name': 'test_project',
        'project_description': 'test project description',
        'project_link': 'github.com/test_project',
        'skills_required': 'python, flask, html',
    }
    response = client.post("/projects", data=project_form)
    with app.app_context():
        project = Projects.query.filter_by(project_name='test_project').first()
        assert response.status_code == 200
        assert project.project_description == 'test project description'
        assert project.project_link == 'github.com/test_project'
        assert project.skills_required == 'python, flask, html'
        assert project.project_status == 'pending'
        assert project.user_id == 1

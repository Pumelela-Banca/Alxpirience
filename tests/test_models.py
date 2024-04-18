"""
Tests models
"""
from expirience.data_base import User, Projects, Skills
from expirience import db

def test_user(app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, 
    and role fields are defined correctly
    """
    user = User(
        username='testuser-2',
        email='test-1@mail.com',
        git_hub='Git-Bob',
        country='Angola',
        password='secret--2'
        )
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        res = User.query.find_by(username="testuser-2")
        assert res.username == 'testuser-2'
        assert res.email == 'test-1@mail.com'
        assert res.git_hub == 'Git-Bob'
        assert res.country == 'Angola'
        assert res.password == 'secret--2'


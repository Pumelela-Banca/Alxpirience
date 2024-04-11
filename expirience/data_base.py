"""
data storage module that uses sqlite
"""
from itsdangerous import TimedSerializer as Serializer
from expirience import db, loginManager
from flask import current_app as app
from flask_login import UserMixin


@loginManager.user_loader
def get_user(user_id):
    """
    returns user by id
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    creates user table or model
    it has id, username, email, country and password
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    git_hub = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    skills = db.relationship('Skills', backref='author', lazy=True)
    projects = db.relationship('Projects', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        gets reset token
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        """
        verifies reset token
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """
        returns a string representation of the user
        """
        return f"User('{self.username}', '{self.email}', '{self.country}', '{self.image_file}', '{self.git_hub}')"


class Skills(db.Model):
    """
    creates skills table or model
    it has id, skill and user_id
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        returns a string representation of the skills
        """
        return f"Skills('{self.skill}')"


class Projects(db.Model):
    """
    creates projects table or model
    it has id, project_name, project_description, project_link and user_id
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_link = db.Column(db.String(120), nullable=False)
    skills_required = db.Column(db.String(120), nullable=False)
    project_status = db.Column(db.String(20), nullable=False, default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        returns a string representation of the projects
        """
        return f"Projects('{self.project_name}', '{self.project_description}', '{self.project_link}', '{self.project_status}')"

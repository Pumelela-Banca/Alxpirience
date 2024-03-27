"""
log-in page details
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from expirience.data_base import User


class RegisterForm(FlaskForm):
    """
    controls log in form
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_field(self, field):
        """
        validates user name uniquesness
        """
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        """
        validates email uniquesness
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    """
    controls log in form
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class UserUpdateForm(FlaskForm):
    """
    controls user update form
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    country = StringField('Country',
                           validators=[DataRequired()])
    #skills = StringField('Skills')
    submit = SubmitField('Update')

    def validate_field(self, field):
        """
        validates user name uniquesness
        """
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        """
        validates email uniquesness
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is taken. Please choose a different one.")


class CreateJobForm(FlaskForm):
    """
    controls job creation form
    """
    job_title = StringField('Job Title',
                           validators=[DataRequired()])
    job_description = TextAreaField('Job Description',
                                    validators=[DataRequired()])
    job_link = StringField('Job Link/Git-Hub Link',
                           validators=[DataRequired()])
    submit = SubmitField('Create Job')

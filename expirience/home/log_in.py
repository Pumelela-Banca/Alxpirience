"""
log-in page details
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from expirience.data_base import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    """
    controls log in form
    """
    AFRICAN_COUNTRIES = ['Algeria','Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde',
                         'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Djibouti',
                         'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia',
                         'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia',
                         'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco',
                         'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe',
                         'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan',
                         'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    git_hub = StringField('GitHub-user-name',
                           validators=[DataRequired()])
    country = SelectField('Select an African Country', choices=AFRICAN_COUNTRIES)
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

    def validate_username(self, username):
        """
        validates user name uniquesness
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken. Please choose a different one.")
        
        
    def validate_email(self, email):
        """
        validates email uniquesness
        """
        if email.data != current_user.email:
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
    skills_required = StringField('Skills Required',
                                 validators=[DataRequired()])
    submit = SubmitField('Create Job')


class SkillsForm(FlaskForm):
    """
    controls skills form
    """
    skill = StringField('Skill',
                        validators=[DataRequired()])
    skill_1 = StringField('Skill-1', default="No")
    skill_2 = StringField('Skill-2', default="No")
    skill_3 = StringField('Skill-3', default="No")
    skill_4 = StringField('Skill-4', default="No")
    submit = SubmitField('Add Skill')

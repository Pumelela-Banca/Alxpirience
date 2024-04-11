"""
Project forms and jobs
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


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

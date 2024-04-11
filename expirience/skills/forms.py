"""
Skills forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SkillsForm(FlaskForm):
    """
    controls skills form
    """
    skill = StringField('Skill',
                        validators=[DataRequired()])
    skill_1 = StringField('Skill-1')
    skill_2 = StringField('Skill-2')
    skill_3 = StringField('Skill-3')
    skill_4 = StringField('Skill-4')
    submit = SubmitField('Add Skill')

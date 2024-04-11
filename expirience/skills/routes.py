"""
routes for the skills pages
"""
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from ..data_base import Skills, db
from .forms import SkillsForm
from flask import Blueprint

skills = Blueprint('skills', __name__)


@skills.route('/addskills', methods=['GET', 'POST'])
@login_required
def addskills():
    """
    renders add skills page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SkillsForm()
    if form.validate_on_submit():
        for val, ky in form.data.items():
            if ky == "skill":
                skill = Skills(skill=val, author=current_user)
                db.session.add(skill)
                db.session.commit()
            elif ky == "skill_1":
                skill = Skills(skill_1=val, author=current_user)
                db.session.add(skill)
                db.session.commit()
            elif ky == "skill_2":
                skill = Skills(skill_2=val, author=current_user)
                db.session.add(skill)
                db.session.commit()
            elif ky == "skill_3":
                skill = Skills(skill_3=val, author=current_user)
                db.session.add(skill)
                db.session.commit()
            elif ky == "skill_4":
                skill = Skills(skill_4=val, author=current_user)
                db.session.add(skill)
                db.session.commit()
        flash('Skills added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('addskills.html', title="Add Skills", form=form)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, Knowledge

knowledge_bp = Blueprint('knowledge', __name__)


@knowledge_bp.route('/')
@login_required
def list_knowledge():
    items = Knowledge.query.filter_by(user_id=current_user.id).all()
    return render_template('knowledge_list.html', items=items)


@knowledge_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_knowledge():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash('Title and content required')
            return redirect(url_for('knowledge.create_knowledge'))
        item = Knowledge(user_id=current_user.id, title=title, content=content)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('knowledge.list_knowledge'))
    return render_template('knowledge_edit.html')

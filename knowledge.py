from flask import Blueprint, request, render_template, redirect, url_for
from models import db, Knowledge
from utils import current_user


bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@bp.route('/')
def list_knowledge():
    user_id = current_user()
    items = Knowledge.query.filter_by(user_id=user_id).all() if user_id else []
    return render_template('knowledge_list.html', items=items)


@bp.route('/new', methods=['GET', 'POST'])
def new_knowledge():
    user_id = current_user()
    if not user_id:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        item = Knowledge(user_id=user_id, title=title, content=content)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('knowledge.list_knowledge'))
    return render_template('knowledge_edit.html')

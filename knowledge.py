from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Knowledge
from utils import login_required

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@knowledge_bp.route('/')
@login_required
def list_knowledge():
    knowledges = Knowledge.query.filter_by(user_id=session['user_id']).all()
    return render_template('knowledge_list.html', knowledges=knowledges)


@knowledge_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_knowledge():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        kn = Knowledge(title=title, content=content, user_id=session['user_id'])
        db.session.add(kn)
        db.session.commit()
        return redirect(url_for('knowledge.list_knowledge'))
    return render_template('knowledge_edit.html', knowledge=None)


@knowledge_bp.route('/<int:kid>/edit', methods=['GET', 'POST'])
@login_required
def edit_knowledge(kid):
    kn = Knowledge.query.get_or_404(kid)
    if request.method == 'POST':
        kn.title = request.form['title']
        kn.content = request.form['content']
        db.session.commit()
        return redirect(url_for('knowledge.list_knowledge'))
    return render_template('knowledge_edit.html', knowledge=kn)


@knowledge_bp.route('/<int:kid>/delete')
@login_required
def delete_knowledge(kid):
    kn = Knowledge.query.get_or_404(kid)
    db.session.delete(kn)
    db.session.commit()
    return redirect(url_for('knowledge.list_knowledge'))

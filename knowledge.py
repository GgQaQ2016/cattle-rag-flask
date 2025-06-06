from flask import Blueprint, request, jsonify, session, render_template
from models import db, Knowledge
from utils import login_required

knowledge_bp = Blueprint('knowledge', __name__)


@knowledge_bp.route('/', methods=['GET'])
@login_required
def list_knowledge():
    records = Knowledge.query.all()
    return render_template('knowledge_list.html', knowledges=records)


@knowledge_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_knowledge():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return jsonify({'error': 'invalid input'}), 400
        record = Knowledge(title=title, content=content, user_id=session['user_id'])
        db.session.add(record)
        db.session.commit()
        return jsonify({'id': record.id})
    return render_template('knowledge_edit.html')


@knowledge_bp.route('/<int:knowledge_id>', methods=['GET'])
@login_required
def get_knowledge(knowledge_id):
    record = Knowledge.query.get_or_404(knowledge_id)
    return jsonify({'id': record.id, 'title': record.title, 'content': record.content})


@knowledge_bp.route('/<int:knowledge_id>', methods=['PUT'])
@login_required
def update_knowledge(knowledge_id):
    record = Knowledge.query.get_or_404(knowledge_id)
    data = request.json
    record.title = data.get('title', record.title)
    record.content = data.get('content', record.content)
    db.session.commit()
    return jsonify({'message': 'updated'})


@knowledge_bp.route('/<int:knowledge_id>', methods=['DELETE'])
@login_required
def delete_knowledge(knowledge_id):
    record = Knowledge.query.get_or_404(knowledge_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'deleted'})

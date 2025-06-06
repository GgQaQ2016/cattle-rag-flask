from flask import Blueprint, request, jsonify, render_template
from models import Knowledge

rag_bp = Blueprint('rag', __name__)


def simple_search(query: str):
    """Very naive search through knowledge content."""
    return Knowledge.query.filter(Knowledge.content.contains(query)).all()


@rag_bp.route('/')
def rag_page():
    """Render a tiny page for making RAG queries."""
    return render_template('rag_query.html')


@rag_bp.route('/query', methods=['POST'])
def rag_query():
    data = request.json
    query = data.get('query', '')
    results = simple_search(query)
    context = "\n".join([k.content for k in results])
    answer = f"[Dummy answer] {query}"
    return jsonify({'answer': answer, 'context': context})

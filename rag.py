from flask import Blueprint, request, render_template
from embeddings.bge_m3 import embed_text
from vector_db.faiss_index import search_vectors


bp = Blueprint('rag', __name__, url_prefix='/rag')


@bp.route('/query', methods=['GET', 'POST'])
def query():
    answer = None
    if request.method == 'POST':
        text = request.form['text']
        vector = embed_text(text)
        docs = search_vectors(vector)
        answer = '\n'.join(docs)
    return render_template('rag_query.html', answer=answer)

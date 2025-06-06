from flask import Blueprint, render_template, request
import openai

from config import Config
from embeddings.bge_m3 import embed_text
from vector_db.faiss_index import FaissIndex

openai.api_key = Config.OPENAI_API_KEY

rag_bp = Blueprint('rag', __name__, url_prefix='/rag')
index = FaissIndex(dim=1536)


@rag_bp.route('/', methods=['GET', 'POST'])
def rag_query():
    if request.method == 'POST':
        question = request.form['question']
        emb = embed_text(question)
        docs = index.search(emb, k=3)
        prompt = question + "\n" + "\n".join(docs)
        completion = openai.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}]
        )
        answer = completion.choices[0].message.content
        return render_template('rag_result.html', answer=answer, docs=docs)
    return render_template('rag_query.html')

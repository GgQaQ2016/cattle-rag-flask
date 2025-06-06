import os
from flask import Blueprint, request, jsonify

upload_bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data')


@upload_bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    file = request.files['file']
    filename = file.filename
    if not filename:
        return jsonify({'error': 'empty filename'}), 400
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    return jsonify({'filename': filename})

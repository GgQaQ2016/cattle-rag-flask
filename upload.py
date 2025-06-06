import os
from flask import Blueprint, render_template, request, url_for, redirect, current_app

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')


@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        f.save(save_path)
        return redirect(url_for('upload.upload_file'))
    return render_template('upload.html')

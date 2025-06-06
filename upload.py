import os
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from werkzeug.utils import secure_filename


bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename:
            filename = secure_filename(f.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            f.save(path)
            return redirect(url_for('upload.upload_file'))
    return render_template('upload.html')

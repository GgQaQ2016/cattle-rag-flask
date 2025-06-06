import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('No file selected')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        flash('File uploaded successfully')
        return redirect(url_for('upload.upload_file'))
    return render_template('upload.html')

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from .models import get_user_by_username

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@main.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Dosya bulunamadı.')
        return redirect(url_for('main.index'))

    file = request.files['file']
    if file.filename == '':
        flash('Dosya seçilmedi.')
        return redirect(url_for('main.index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('Dosya yüklendi.')
        return redirect(url_for('main.index'))

    flash('Geçersiz dosya türü.')
    return redirect(url_for('main.index'))

@main.route('/delete/<filename>')
def delete(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Dosya silindi.')
    else:
        flash('Dosya bulunamadı.')
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Giriş başarılı.')
            return redirect(url_for('main.index'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Çıkış yapıldı.')
    return redirect(url_for('main.index'))
    

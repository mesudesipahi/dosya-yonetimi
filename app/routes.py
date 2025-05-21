import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegisterForm, LoginForm
from .models import User, users, get_user_by_username, get_user_by_id
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if get_user_by_username(form.username.data):
            flash('Bu kullanıcı adı zaten alınmış.')
            return redirect(url_for('main.register'))
        user_id = str(len(users) + 1)
        hashed_password = generate_password_hash(form.password.data)
        user = User(user_id, form.username.data, hashed_password)
        users[user_id] = user
        flash('Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.upload'))
        flash('Hatalı kullanıcı adı veya şifre.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.')
    return redirect(url_for('main.login'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Dosya bulunamadı.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Dosya seçilmedi.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            flash('Dosya başarıyla yüklendi.')
            return redirect(url_for('main.upload'))
        else:
            flash('Yalnızca PDF, PNG veya JPG dosyaları kabul edilir.')
            return redirect(request.url)
    return render_template('upload.html')
@main.route('/files')
@login_required
def files():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_folder)
    return render_template('files.html', files=files)
@main.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'{filename} silindi.')
    else:
        flash('Dosya bulunamadı.')
    return redirect(url_for('main.files'))
    

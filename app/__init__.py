import os
from flask import Flask, send_from_directory
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'  # Gerçek bir uygulamada .env dosyasına al!

    # Dosya yükleme ayarları
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg'}

    # uploads klasörü yoksa oluştur
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Blueprint'i kaydet
    from .routes import main
    app.register_blueprint(main)

    # Flask-Login yapılandırması
    login_manager.init_app(app)

    # Yüklenen dosyaların erişilebilir olması için route (Görüntüle linki için)
    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app


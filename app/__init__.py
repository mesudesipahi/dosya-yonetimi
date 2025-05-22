from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Yükleme klasörünü ayarla
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    
    # Gizli anahtar (flash mesajları, oturum vb. için)
    app.secret_key = 'gizli-anahtar'

    # Yükleme klasörü yoksa oluştur
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Blueprint kayıt
    from .routes import main
    app.register_blueprint(main)

    return app



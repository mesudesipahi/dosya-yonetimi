from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message="Kullanıcı adı gerekli."),
        Length(min=3, max=25, message="Kullanıcı adı 3 ile 25 karakter arasında olmalı.")
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message="E-posta gerekli."),
        Email(message="Geçerli bir e-posta giriniz.")
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message="Şifre gerekli."),
        Length(min=6, message="Şifre en az 6 karakter olmalı.")
    ])
    confirm_password = PasswordField('Şifre Tekrar', validators=[
        DataRequired(message="Lütfen şifrenizi tekrar girin."),
        EqualTo('password', message="Şifreler eşleşmiyor.")
    ])
    submit = SubmitField('Kayıt Ol')

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(message="Kullanıcı adı gerekli.")])
    password = PasswordField('Şifre', validators=[DataRequired(message="Şifre gerekli.")])
    submit = SubmitField('Giriş Yap')

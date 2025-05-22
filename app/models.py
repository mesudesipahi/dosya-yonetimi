from flask_login import UserMixin

# Basit kullanıcı modeli
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# Basit kullanıcı veritabanı 
users = {}

# Kullanıcıyı ID'ye göre getirir.
def get_user_by_id(user_id):
    return users.get(user_id)

# Kullanıcıyı kullanıcı adına göre getirir.
def get_user_by_username(username):
    return next((user for user in users.values() if user.username == username), None)

# Kullanıcıyı e-postaya göre getirir
def get_user_by_email(email):
    return next((user for user in users.values() if user.email == email), None)

# Yeni kullanıcı ekleme
def add_user(username, email, password):
    user_id = str(len(users) + 1)
    new_user = User(user_id, username, email, password)
    users[user_id] = new_user
    return new_user

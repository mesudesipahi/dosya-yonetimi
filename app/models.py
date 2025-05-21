from flask_login import UserMixin

# Basit bir kullanıcı modeli (şimdilik sadece username ve password saklayacağız)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Basit veritabanı (örnek için dictionary)
users = {}

# Kullanıcıyı ID'ye göre getirme
def get_user_by_id(user_id):
    return users.get(user_id)

# Kullanıcıyı kullanıcı adına göre getirme
def get_user_by_username(username):
    for user in users.values():
        if user.username == username:
            return user
    return None

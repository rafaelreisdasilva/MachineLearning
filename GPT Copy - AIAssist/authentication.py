from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

# Dummy user data (replace with actual user data or database )
users = {
    'username': generate_password_hash('123')
}

# Authentication verification function
@auth.verify_password
def verify_password(username, password):
    hashed_password = users.get(username)
    if hashed_password and check_password_hash(hashed_password, password):
        return username

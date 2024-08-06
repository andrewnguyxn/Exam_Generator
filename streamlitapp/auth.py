from db import create_connection, get_user, add_user

def authenticate(username, password):
    correct_username = 'test'
    correct_password = 'test'
    
    if username == correct_username and password == correct_password:
        return {"username": correct_username, "role": "user"}
    else:
        return None

def create_new_user(username, password, role):
    conn = create_connection('users.db')
    add_user(conn, username, password, role)
    conn.close()
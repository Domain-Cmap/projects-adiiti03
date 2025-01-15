from db import insert_into_users, get_all_users_data

def create_user(name, password):
    insert_into_users(name, password)

def check_name_availability(name):
    return all(user[1] != name for user in get_all_users_data())

def check_login_validity(name, password):
    return any(user[1] == name and user[2] == password for user in get_all_users_data())

def get_user_id(name):
    return next((user[0] for user in get_all_users_data() if user[1] == name), None)

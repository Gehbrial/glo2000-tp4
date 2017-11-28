from hashlib import sha256

import os


def hash_user_password(password):
    hashed_text = sha256(password.encode()).hexdigest()
    return hashed_text


def get_user_folder_path(username):
    return os.path.join('users', username)


def user_exists(username):
    return os.path.isdir(get_user_folder_path(username))


def create_user(username, password):

    if not os.path.isdir('users'):
        os.mkdir('users')

    if user_exists(username):
        raise ValueError("L'utilisateur {} existe deja".format(username))

    # Creation du dossier de l'utilisateur
    user_path = get_user_folder_path(username)
    os.mkdir(user_path)

    config_path = os.path.join(user_path, 'config.txt')

    with open(config_path, 'w') as config_file:
        config_file.write(hash_user_password(password))

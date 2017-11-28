from hashlib import sha256

import os


def init():
    if not os.path.isdir('users'):
        os.mkdir('users')


def _hash_user_password(password):
    hashed_text = sha256(password.encode()).hexdigest()
    return hashed_text


def _read_user_password(username):
    config_pth = os.path.join(_get_user_folder_path(username), 'config.txt')
    with open(config_pth, 'rU') as infile:
        return infile.read()


def _get_user_folder_path(username):
    return os.path.join('users', username)


def _user_exists(username):
    return os.path.isdir(_get_user_folder_path(username))


def create_user(username, password):
    init()

    if _user_exists(username):
        raise ValueError("L'utilisateur {} existe deja".format(username))

    # Creation du dossier de l'utilisateur
    user_path = _get_user_folder_path(username)
    os.mkdir(user_path)

    config_path = os.path.join(user_path, 'config.txt')

    with open(config_path, 'w') as config_file:
        config_file.write(_hash_user_password(password))


def validate_password(username, password):
    init()
    if not _user_exists(username):
        raise ValueError("L'utilisateur {} n'existe pas".format(username))

    actual = _hash_user_password(password)
    expected = _read_user_password(username)

    return actual == expected

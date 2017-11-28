from hashlib import sha256

import os
import re

PASSWORD_PATTERN = re.compile("^(?=.*[A-Za-z])(?=.*\d).{6,12}$")


def _enforce_password_rules(password):
    if not PASSWORD_PATTERN.match(password):
        raise ValueError(
            "Le mot de passe doit être en 6 et 12 caracteres et doit comporter une lettre ainsi qu'un chiffre"
        )


def _hash_user_password(password):
    hashed_text = sha256(password.encode()).hexdigest()
    return hashed_text


def _read_user_password(username):
    config_pth = os.path.join(username, 'config.txt')
    with open(config_pth, 'rU') as infile:
        return infile.read()


def _user_exists(username):
    return os.path.isdir(username)


def create_user(username, password):

    if _user_exists(username):
        raise ValueError("L'utilisateur {} existe deja".format(username))

    _enforce_password_rules(password)

    # Creation du dossier de l'utilisateur
    os.mkdir(username)

    config_path = os.path.join(username, 'config.txt')

    with open(config_path, 'w') as config_file:
        config_file.write(_hash_user_password(password))


def validate_password(username, password):
    if not _user_exists(username):
        raise ValueError("L'utilisateur {} n'existe pas".format(username))

    actual = _hash_user_password(password)
    expected = _read_user_password(username)

    return actual == expected

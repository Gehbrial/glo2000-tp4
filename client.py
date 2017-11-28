from getpass import getpass

from menu import Menu

from socket_util import rcv_msg, snd_msg


import argparse
import socket


class EmailClient(object):

    def __init__(self, destination, port):
        self._dest = (destination, port)

    def _send_message(self, msg_type, *args):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self._dest)
        snd_msg(s, ';'.join([msg_type] + [str(arg) for arg in args]))

        response = rcv_msg(s)
        s.close()

        header, *body = response.split(';')

        if header == 'ERROR':
            print('Une erreur est survenue: "{}"'.format(body[0]))

    def _register(self, username, password):
        self._send_message('REGISTER', username, password)

    def create_account(self):
        username = input("Entrer votre nom d'utilisateur: ")
        password = getpass("Entrer votre mot de passe: ")
        self._register(username, password)


def login():
    print('Choice: world')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', '-d', default='localhost')
    parser.add_argument('--port', '-p', type=int, default=1337)
    parsed_args = parser.parse_args()

    client = EmailClient(parsed_args.dest, parsed_args.port)

    items = {
        'Se connecter': login,
        'Creer un compte': client.create_account
    }
    main_menu = Menu('Menu de connexion', items)

    main_menu.show()
    main_menu.get_input()

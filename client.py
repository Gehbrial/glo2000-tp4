#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from menu import Menu

from socket_util import rcv_msg, snd_msg


import argparse
import socket
import ast


class EmailClient(object):

    def __init__(self, destination, port):
        self._dest = (destination, port)
        self._auth_token = None

    def _send_message(self, msg_type, *args):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self._dest)

        if self._auth_token is not None:
            args = list(args)
            args.append(self._auth_token)

        snd_msg(s, ';'.join([msg_type] + [str(arg) for arg in args]))

        response = rcv_msg(s)
        s.close()

        header, *body = response.split(';')

        if header == 'ERROR':
            raise Exception('Une erreur est survenue: "{}"'.format(body[0]))

        return header, body

    @staticmethod
    def _get_user_credentials():
        username = input("Entrer votre nom d'utilisateur: ")
        password = getpass("Entrer votre mot de passe: ")

        return username, password

    def create_account(self):
        self._send_message('REGISTER', *EmailClient._get_user_credentials())

    def login(self):
        out = self._send_message('LOGIN', *EmailClient._get_user_credentials())
        header, tkn_container = out

        if header == 'BAD_PASSWORD':
            print('Mot de passe invalide')
            return

        self._auth_token = tkn_container[0]

        self.email_main_menu()

    def email_main_menu(self):

        submenu_items = {
            'Envoi de courriels': self.send_email,
            'Consultation de courriels': self.consult_emails,
            'Statistiques': lambda: 1,
            'Quitter': lambda: 1
        }

        while True:
            m = Menu('Menu Principal', submenu_items)
            m.show()
            m.get_input()

    def send_email(self):
        dest_email = input("Entrer l'adresse de destination: ")
        subject = input('Entrer le sujet du message: ')
        body = input('Entrer le corps du message: ')
        header, body = self._send_message('SEND_MAIL', dest_email, subject, body)

    def consult_emails(self):
        header, data = self._send_message('CONSULT_EMAILS')

        if header == 'OK':
            messages = ast.literal_eval(data[0])

            if bool(messages):
                items = {}

                for k, v in messages.items():
                    items[v] = lambda key=k: self.get_email_content(key)

                m = Menu('Sélectionnez le courriel à afficher', items)
                m.show()
                m.get_input()
            else:
                print('Aucun courriel trouvé')

    def get_email_content(self, k):
        header, data = self._send_message('GET_EMAIL_CONTENT', k)
        title = "Contenu du message"

        print("\n")
        print(title)
        print('-' * len(title) + "\n")
        print(data[0] + "\n")
        input("Appuyez sur une touche pour continuer... ")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', '-d', default='localhost')
    parser.add_argument('--port', '-p', type=int, default=1337)
    parsed_args = parser.parse_args()

    client = EmailClient(parsed_args.dest, parsed_args.port)

    items = {
        'Se connecter': client.login,
        'Creer un compte': client.create_account
    }
    main_menu = Menu('Menu de connexion', items)

    while True:
        main_menu.show()
        main_menu.get_input()

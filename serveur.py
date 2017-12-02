from mail import send_email, retrieve_user_emails, get_email_content

from socket_util import rcv_msg, snd_msg

from user import create_user, validate_password, hash_text


import argparse
import os
import socket


SERVER_SECRET = os.getenv('SERVER_SECRET', 'some_app_secret')


class MailServer(object):

    def __init__(self):
        self._connection_count = 0

    @staticmethod
    def _get_socket():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return server_socket

    @staticmethod
    def _error(err, s):
        snd_msg(s, 'ERROR;' + str(err))

    @staticmethod
    def _ok(s):
        snd_msg(s, 'OK')

    @staticmethod
    def _generate_token(username):
        concat = SERVER_SECRET + username
        token = hash_text(concat)
        return '{0}:{1}'.format(username, token)

    @staticmethod
    def _validate_token(tkn):
        username, expected_hash = tkn.split(':')
        actual_hash = MailServer._generate_token(username)
        return actual_hash != expected_hash

    def start(self, port):
        server_socket = MailServer._get_socket()
        server_socket.bind(('localhost', port))
        server_socket.listen(5)

        while True:
            print('En attente de connexions..')
            (s, address) = server_socket.accept()
            self._connection_count += 1
            self.handle_connection(s)
            s.close()

    def handle_connection(self, s):
        msg = rcv_msg(s)
        # TODO: Handle error if len(msg.split) = 0
        msg_type, *body = msg.split(';')

        try:
            if msg_type == 'REGISTER':
                # TODO: Handle if len body != 2
                (username, password) = body
                create_user(username, password)
                self._ok(s)

            elif msg_type == 'LOGIN':
                # TODO: Handle if len body != 2
                (username, password) = body
                ok = validate_password(username, password)

                if ok:
                    snd_msg(s, 'OK;{}'.format(MailServer._generate_token(username)))
                else:
                    snd_msg(s, 'BAD_PASSWORD')

            elif msg_type == 'SEND_MAIL':
                dest, subject, body, token = body

                if MailServer._validate_token(token):
                    send_email(dest, subject, body, token.split(':')[0])
                    self._ok(s)
                else:
                    self._error('acces refuse', s)
            elif msg_type == 'CONSULT_EMAILS':
                username = body[0].split(':')[0]
                messages = retrieve_user_emails(username)
                snd_msg(s, 'OK;{}'.format(messages))
            elif msg_type == 'GET_EMAIL_CONTENT':
                username = body[1].split(':')[0]
                index = body[0]
                content = get_email_content(username, index)
                snd_msg(s, 'OK;{}'.format(content))

        except Exception as e:
            self._error(e, s)

        s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=1337)

    args = parser.parse_args()

    print('Demarrage du serveur...')
    server = MailServer()
    server.start(port=args.port)

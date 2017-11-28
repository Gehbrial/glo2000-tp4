from socket_util import rcv_msg, snd_msg
from user import create_user


import argparse
import socket


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
                self.register(username, password)

        except Exception as e:
            self._error(e, s)

        self._ok(s)

        s.close()

    def register(self, username, password):
        create_user(username, password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=1337)

    args = parser.parse_args()

    print('Demarrage du serveur...')
    server = MailServer()
    server.start(port=args.port)

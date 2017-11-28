import struct


def recvall(s, count):
    buf = b""
    while count > 0:
        newbuf = s.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def snd_msg(s, message):
    message = message.encode()
    s.sendall(struct.pack('!I', len(message)))
    s.sendall(message)


def rcv_msg(s):
    length, = struct.unpack('!I', recvall(s, 4))
    return recvall(s, length).decode()
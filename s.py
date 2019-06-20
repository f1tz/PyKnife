# -*- coding: utf-8 -*-
import socket
import chardet


def server(ip, addr):
    s = socket.socket()
    s.bind((ip, addr))
    s.listen()
    print('[+]Listen on %s:%s' % (ip, addr))
    c, caddr = s.accept()
    print('[+]Connected from %s:%s' % caddr)
    r = c.recv(1024)
    codetype = chardet.detect(r)['encoding']
    print(r.decode(codetype))

    while True:
        x = input()  # bugs
        while x == '':
            x = input()
        c.send(x.encode())
        data = c.recv(1024)
        codetype = chardet.detect(data)['encoding']
        data = data.decode(codetype)
        print(data)

    s.close()


if __name__ == '__main__':
    server('127.0.0.1', 7788)

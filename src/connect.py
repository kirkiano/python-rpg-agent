import socket
import json


class Connection(object):

    class CannotAuthenticate(Exception):
        def __init__(self):
            self.msg = 'Cannot authenticate with given credentials'

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((host, port))
        self.sockin = self.socket.makefile('r')
        self.sockout = self.socket.makefile('w')

    def send_message(self, m):
        j = json.dumps(m)
        j = j + '\n'
        self.sockout.writelines([j])
        self.sockout.flush()

    def recv_message(self):
        line = self.sockin.readline()
        j = json.loads(line)
        return j

    def close(self):
        self.sockin = self.sockout = None
        self.socket.close()

    def authenticate(self, user, pw):
        self.send_message({
            'type': 'login',
            'creds': {'user': user, 'pass': pw}
        })
        resp = self.recv_message()
        if (('type' not in resp) or ('value' not in resp) or
                (resp['type'] != 'auth') or (resp['value'] != 'Welcome')):
            raise Connection.CannotAuthenticate()

    def look(self):
        self.send_message({'type': 'whereami'})

    def take_exit(self, eid):
        self.send_message({'type': 'exit', 'eid':  eid})

    def say(self, s):
        self.send_message({'type': 'say', 'value': s})

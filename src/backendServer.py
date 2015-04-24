import socket, threading

from loader import config

class Backend:

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', config.port))
        self.server.listen(1)

    def defaultOnMessage(self, data):
        print 'meessage recieved: ' + data

    def start(self):
        conn, addr = self.server.accept()
        print 'Connected by', addr
        while 1:
            data = conn.recv(1024)
            conn.sendall(data)
        conn.close()

class BackendThread(threading.Thread):

    def __init__(self):
        self.setCallback(self.defaultCallback)

    def setCallback(self, callback):
        self.callback = callback

    def defaultCallback(self, data):
        print 'message: ', data

    def onConnected(self, addr):
        print 'connected:', addr

    def run(self):
        self.running = True

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', config.port))
        self.server.listen(1)
        conn, addr = self.server.accept()
        self.onConnected(addr)

        while True:
            try:
                conn, address = self.server.accept()
                while True:
                    data = conn.recv(1024)
                    self.callback(data)
            except socket.error, exc:
                print "Caught exception socket.error : %s" % exc
            finally:
                if not self.running:
                    conn.close()

    def terminate(self):
        self.running = False
        self.server.close()

if __name__ == '__main__':
    server = BackendThread()
    server.run()
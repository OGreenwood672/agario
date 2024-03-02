import socket
import pickle


class Network:
    def __init__(self): # initilizes player object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server =  socket.gethostbyname(socket.gethostname())
        self.port = 6720
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def connect(self): # connects to server
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data): # allows client to send data to server
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as e:
            print(e)
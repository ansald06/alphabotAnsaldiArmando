import socket
from threading import Thread

MY_ADDRESS = ("192.168.1.112", 9000)
BUFFER_SIZE = 4096

class Receive(Thread):
    def __init__(self, s):
        super().__init__()
        self.s = s
        self.running = True
        self.sender_address= None
        self.clients= {}
    def run(self):
        while self.running:
            data, self.sender_address = self.s.recvfrom(BUFFER_SIZE)
            if self.sender_address not in self.clients:
                self.clients[self.sender_address]=self.sender_address
            string = data.decode()
            print(f"{self.sender_address}: {string}")
            
    def kill(self):
        self.running = False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(MY_ADDRESS)
    
    # Starting thread
    receiver = Receive(s)
    receiver.start()

    while True:
        # Send message
        if receiver.sender_address != None:
            for address in receiver.clients:
                string = input("-> ")
                binary_string = string.encode()
                s.sendto(binary_string, receiver.clients[address])

if __name__ == "__main__":
    main()

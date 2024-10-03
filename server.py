import socket
from threading import Thread

MY_ADDRESS = ("0.0.0.0", 9000)  # Ascolta su tutte le interfacce
BUFFER_SIZE = 4096

class Receive(Thread):
    def __init__(self, conn, address):
        super().__init__()
        self.conn = conn
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.conn.recv(BUFFER_SIZE)
                if data:
                    string = data.decode()
                    print(f"Ricevuto da {self.address}: {string}")
                    
                    # Esegui qui la tua logica per determinare la risposta
                    if "hello" in string.lower():
                        response = "okay|Saluto ricevuto"
                    else:
                        response = "error|Frase sconosciuta"

                    # Invia la risposta al client
                    self.conn.sendall(response.encode())
                else:
                    break
            except ConnectionResetError:
                break

    def kill(self):
        self.running = False
        self.conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
    s.bind(MY_ADDRESS)
    s.listen(5)  # Ascolta fino a 5 connessioni simultanee

    print("Server in ascolto...")

    while True:
        conn, address = s.accept()  # Accetta una nuova connessione
        print(f"Connessione accettata da {address}")

        # Inizia un thread separato per gestire ciascun client
        receiver = Receive(conn, address)
        receiver.start()

        while True:
            string = input("-> ")
            if string.lower() == "exit":
                break
            binary_string = string.encode()
            conn.sendall(binary_string)

if __name__ == "__main__":
    main()

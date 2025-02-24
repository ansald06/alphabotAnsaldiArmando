'''
    MOVIMENTO CON COMANDO E TEMPO DI ESECUZIONE
'''
import socket 

SERVER_ADDRESS = ("192.168.1.137", 8000) #indirizzo ip del server 
BUFFER_SIZE = 4096

def main(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(SERVER_ADDRESS)

    while True: 
        comando = input(f"Inserisci un comando(forward, backward, left, right): ")
        value = input(f"Inserisci un valore di tempo in millisecondi: ")
        s.sendall((f"{comando}|{value}").encode()) #manda messaggio dei due valori separato da |
        message = s.recv(BUFFER_SIZE)
        ricevuto = message.decode()
        status = ricevuto.split("|")[0] #divide il messaggio rispetto la | 
        phrase = ricevuto.split("|")[1]
        print(f"stato:{status}")
        print(f"phrase:{phrase}")
    s.close()   
    
if __name__ == "__main__":
    main()

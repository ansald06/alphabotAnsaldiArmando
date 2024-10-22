'''
    MOVIMENTO CON WASD SENZA L'HEARTBEAT DI CONTROLLO
'''
import socket
from AlphaBot import AlphaBot  

#dizionario dei comandi che può fare associati alle lettere WASD 
diz_command = {
    "W": "avanti",
    "S": "indietro",
    "A": "sinistra",
    "D": "destra",
    "E": "ferma"
}

MYADDRESS = ("192.168.1.137", 8000) #indirizzo ip del server
BUFFER_SIZE = 4096

def main():
    bot = AlphaBot()
    bot.stop() #necessario per assicurarsi che sia fermo quando iniziamo ad eseguire

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    while True:
        command = connection.recv(BUFFER_SIZE).decode() #decodifica il comando ricevuto
        #print(command)
        if command in diz_command: #controlla se il comando è nel dizionario 
            status = "ok"
            phrase = diz_command[command]
            
            if command == 'W': #controlla quale comando deve fare
                #print(command)
                bot.forward() #chiama la funzione per il movimento della classe alpahbot
            elif command == 'S':
                bot.backward()
            elif command == 'A':
                bot.left()
            elif command == 'D':
                bot.right()
            elif command == 'E': #se si clicca la E si ferma 
                bot.stop()

        else:
            status = "error"
            phrase = "comando non trovato"

        answer = f"{status}|{phrase}" #risponde con la frase al client 
        connection.send(answer.encode())

if __name__ == '__main__':
    main()

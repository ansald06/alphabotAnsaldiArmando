'''
    MOVIMENTO CON COMANDO E TEMPO DI ESECUZIONE
'''
import socket
from AlphaBot import AlphaBot  
import time

#dizionario dei comandi che può fare
diz_command = {
    "forward": "avanti",
    "backward": "indietro",
    "left": "sinistra",
    "right": "destra",
    "stop": "ferma"
}

MYADDRESS = ("192.168.1.137", 8000) #indirizzo ip del server 
BUFFER_SIZE = 4096

def main():
    bot = AlphaBot()
    bot.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    while True:        
        message = connection.recv(BUFFER_SIZE).decode()
        command, value = message.split('|')
        print(f"Comando: {command}, Valore: {value}") #stampa il comando e il tempo che ha ricevuto

        if command in diz_command: #controlla se il comando è nel dizionario 
            status = "ok"
            phrase = diz_command[command]

            if command == "forward": #controlla quale comando deve fare
                bot.forward() #chiama la funzione per il movimento della classe alpahbot
            elif command == "backward":
                bot.backward()
            elif command == "left":
                bot.left()
            elif command == "right":
                bot.right()
            elif command == "stop":
                bot.stop()

            time.sleep(int(value)) #sleep del tempo che deve eseguire un movimento ricevuto dal client
            bot.stop() #ferma l'alphabot per un nuovo comando

        else:
            status = "error"
            phrase = "comando non trovato"

        answer = f"{status}|{phrase}" #risponde con la frase al client 
        connection.send(answer.encode())

if __name__ == '__main__':
    main()

'''
    MOVIMENTO CON WASD CON L'HEARTBEAT DI CONTROLLO
'''
import socket
from AlphaBot import AlphaBot  
import time
import threading

#dizionario dei comandi che può fare associati alle lettere WASD 
diz_command = {
    "W": "avanti",
    "S": "indietro",
    "A": "sinistra",
    "D": "destra",
    "E": "ferma"
}

MYADDRESS = ("192.168.1.137", 8000) #indirizzo ip del server
HEARTBEAT_ADDRESS = ("192.168.1.137", 9000) #indirizzo ip del hertbeat che è lo stesso del server ma con un'altra porta
BUFFER_SIZE = 4096


socket_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_command.bind(MYADDRESS)
socket_heartbeat.bind(HEARTBEAT_ADDRESS)

socket_command.listen(1)
socket_heartbeat.listen(1)
print("server TCP in attesa di connesioni")

recive_command, address1 = socket_command.accept()
print("connesione client")
recive_heartbeat, address2 = socket_command.accept()
print("connesione heartbeat")

def hearthbeat_recive(recive_heartbeat):
    socket_heartbeat.settimeout(6.5)
    while True:
        try:
            data = recive_heartbeat.recv(4092)
            print("up")
        except socket.timeout:
            print("FERMA TUTTO")
            break
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break

    socket_command.close()
    socket_heartbeat.close()


def heartbeat_send(recive_heartbeat):
    while True:
        try:
            recive_heartbeat.sendall(b"heartbeat")
            time.sleep(6)  # invia un heartbeat ogni 6 secondi
        except Exception as e:
            print(f"Errore nell'invio heartbeat: {e}")
            break

#avvio del thread per inviare heartbeat
thread_send_heartbeat = threading.Thread(target=heartbeat_send, args=(recive_heartbeat,))
thread_send_heartbeat.start()

#avvio del thread per ricevere heartbeat
thread_receive_heartbeat = threading.Thread(target=hearthbeat_recive, args=(recive_heartbeat,))
thread_receive_heartbeat.start()

def main():
    bot = AlphaBot()
    bot.stop() #necessario per assicurarsi che sia fermo quando iniziamo ad eseguire

    while True:
        command = recive_command.recv(BUFFER_SIZE).decode() #decodifica il comando ricevuto
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
        recive_command.send(answer.encode())

if __name__ == '__main__':
    main()

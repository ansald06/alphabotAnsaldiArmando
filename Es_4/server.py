import socket
import time
import threading
import sqlite3
from AlphaBot import AlphaBot  

# dizionario dei comandi che può fare associati alle lettere WASD 
diz_command = {
    "W": "avanti",
    "S": "indietro",
    "A": "sinistra",
    "D": "destra",
    "E": "ferma"
}

MYADDRESS = ("192.168.1.137", 8000)  # Indirizzo IP del server
HEARTBEAT_ADDRESS = ("192.168.1.137", 9000)  # Porta separata per heartbeat
BUFFER_SIZE = 4096

# Configurazione dei socket
socket_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_command.bind(MYADDRESS)
socket_heartbeat.bind(HEARTBEAT_ADDRESS)

socket_command.listen(1)
socket_heartbeat.listen(1)
print("Server TCP in attesa di connessioni")

receive_command, address = socket_command.accept()
print("Connessione client")
receive_heartbeat, address2 = socket_heartbeat.accept()
print("Connessione heartbeat")


def heartbeat_receive():
    socket_heartbeat.settimeout(6.5)
    while True:
        data = receive_heartbeat.recv(BUFFER_SIZE)
        if not data:
            print("FERMA TUTTO")
            break
        print("Heartbeat ricevuto")

def heartbeat_send():
    while True:
        receive_heartbeat.sendall(b"heartbeat")
        time.sleep(6)  # invia un heartbeat ogni 6 secondi

#avvio del thread per inviare heartbeat
thread_receive_heartbeat = threading.Thread(target=heartbeat_receive)
thread_receive_heartbeat.start()

#avvio del thread per ricevere heartbeat
thread_send_heartbeat = threading.Thread(target=heartbeat_send)
thread_send_heartbeat.start()


# Funzione per cercare un comando nel database
def query_database(command):
    conn = sqlite3.connect('mio_database.db')
    cursor = conn.cursor()

    stringa = f"SELECT str_mov FROM comandi WHERE comando = '{command}'"
    print(stringa)
    cursor.execute(stringa)
    conn.commit()

    mov_sequence = cursor.fetchone()
    conn.close()
    return mov_sequence

# Funzione per eseguire la sequenza di movimenti dal database
def execute_mov_sequence(database_mov, bot):
    str_mov = database_mov[0]
    mov_list = str_mov.split(',')
    
    for move in mov_list:
        direction = move[0]  # Comando 
        duration = int(move[1:])  # Tempo

        if direction == 'F':
            bot.forward()
        elif direction == 'B':
            bot.backward()
        elif direction == 'L':
            bot.left()
        elif direction == 'R':
            bot.right()

        print(f"movimento: {direction}, durata: {duration} ms")
        time.sleep(duration / 1000)  # Converti i millisecondi in secondi

        bot.stop()

def main():
    bot = AlphaBot()
    bot.stop() #necessario per assicurarsi che sia fermo quando iniziamo ad eseguire

    while True:
        command = receive_command.recv(BUFFER_SIZE).decode()  # decodifica il comando ricevuto
        print(f"comando ricevuto: {command}")

        if command in diz_command:  # controlla se il comando è nel dizionario 
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

            print(f"eseguo comando: {phrase}")
        else: 
            #cerca il comando nel database
            database_mov = query_database(command)
            if database_mov:  # Se il comando è nel database
                status = "ok"
                phrase = f"sequenza dal database: {database_mov}"
                print(f"sequenza comando database trovata: {database_mov}")
                #execute_mov_sequence(database_mov) #esegue la sequenza del DB
                execute_mov_sequence(database_mov, bot)
            else:
                status = "error"
                phrase = "comando non trovato"
                print("Comando non trovato nel database")

        #risponde al client con lo stato e la frase
        answer = f"{status}|{phrase}"
        receive_command.send(answer.encode())

if __name__ == '__main__':
    main()

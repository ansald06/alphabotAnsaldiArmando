'''
    MOVIMENTO CON WASD SENZA L'HEARTBEAT DI CONTROLLO
'''
import socket
from pynput import keyboard

SERVER_ADDRESS = ("192.168.1.137", 8000) #indirizzo ip del server 
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

#dizionario per far si che si manda una sola volta il messaggio che è stato premuto un pulsante 
# se no vengono inviati troppi messaggi mentre si tiene premuto il tasto
buttons = {
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "e": False
}

def on_press(key): #funzione per rilevare la pressione dei tasti
    if key.char == "w" and not buttons["w"]: #controlla che non sia già premuto cosi manda un solo messaggio
        print("premuto w")
        buttons["w"] = True #mettendo a true vuol dire che è premuto cosi manda un solo messaggio
    elif key.char == "s" and not buttons["s"]:
        print("premuto s")
        buttons["s"] = True 
    elif key.char == "a" and not buttons["a"]:
        print("premuto a")
        buttons["a"] = True  
    elif key.char == "d" and not buttons["d"]:
        print("premuto d")
        buttons["d"] = True  
    elif key.char == "e" and not buttons["e"]:
        print("premuto e")
        buttons["e"] = True 

    s.sendall((key.char.upper()).encode()) #manda la lettera maiuscola al server 


def on_release(key): #funzione per rilevare il rilascio dei tasti
    if key.char == "w" and buttons["w"]: #controlla se è premuto 
        print("rilascito w")
        buttons["w"] = False #imposta a false che significa che è stato rilasciato
    elif key.char == "s" and buttons["s"]:
        print("rilascito s")
        buttons["s"] = False  
    elif key.char == "a" and buttons["a"]:
        print("rilascito a")
        buttons["a"] = False  
    elif key.char == "d" and buttons["d"]:
        print("rilascito d")
        buttons["d"] = False  
    elif key.char == "e" and buttons["e"]:
        print("rilascito e")
        buttons["e"] = False  

    s.sendall("E".encode()) #quando rilascio un tasto manda E che ferma l'alphabot


def main():
    with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join() 

    message = s.recv(BUFFER_SIZE)
    answer_server = message.decode()
    status, phrase = answer_server.split("|") #divide e stampa il messaggio ricevuto dal server in risposta al movimento
    print(f"stato: {status}")
    print(f"phrase: {phrase}")

if __name__ == "__main__":
    main()

'''
    MOVIMENTO CON WASD E CON COMANDI DA DB E L'HEARTBEAT DI CONTROLLO
'''

import socket
import threading
from pynput import keyboard

buttons = {
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "e": False,
    "q": False,
    "f": False,
    "z": False
}

SERVER_ADDRESS = ("192.168.1.137", 8000)  #indirizzo IP del server 
HEARTBEAT_ADDRESS = ("192.168.1.137", 9000)
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(SERVER_ADDRESS)
heartbeat_socket.connect(HEARTBEAT_ADDRESS)

def on_press(key):
    if key.char == "w" and not buttons["w"]:
        #print("premuto w")
        buttons["w"] = True
    elif key.char == "s" and not buttons["s"]:
        #print("premuto s")
        buttons["s"] = True 
    elif key.char == "a" and not buttons["a"]:
        #print("premuto a")
        buttons["a"] = True  
    elif key.char == "d" and not buttons["d"]:
        #print("premuto d")
        buttons["d"] = True  
    elif key.char == "e" and not buttons["e"]:
        #print("premuto e")
        buttons["e"] = True 
    elif key.char == "q" and not buttons["q"]: 
        #print("Premuto q")
        buttons["q"] = True
    elif key.char == "f" and not buttons["f"]: 
        #print("Premuto f")
        buttons["f"] = True
    elif key.char == "z" and not buttons["z"]: 
        #print("Premuto f")
        buttons["z"] = True

    s.sendall((key.char.upper()).encode())
    
    message = s.recv(BUFFER_SIZE)
    answer_server = message.decode()
    status, phrase = answer_server.split("|")
    print(f"Stato: {status}")
    print(f"Frase: {phrase}")

def on_release(key):
    if key.char == "w" and buttons["w"]: #controlla se è premuto 
        #print("rilascito w")
        buttons["w"] = False #imposta a false che significa che è stato rilasciato
    elif key.char == "s" and buttons["s"]:
        #print("rilascito s")
        buttons["s"] = False  
    elif key.char == "a" and buttons["a"]:
        #print("rilascito a")
        buttons["a"] = False  
    elif key.char == "d" and buttons["d"]:
        #print("rilascito d")
        buttons["d"] = False  
    elif key.char == "e" and buttons["e"]:
        #print("rilascito e")
        buttons["e"] = False  
    elif key.char == "q" and buttons["q"]:  
        #print("Rilasciato q")
        buttons["q"] = False
    elif key.char == "f" and buttons["f"]:  
        #print("Rilasciato f")
        buttons["f"] = False
    elif key.char == "z" and buttons["z"]:  
        #print("Rilasciato f")
        buttons["z"] = False

    s.sendall("E".encode()) #quando rilascio un tasto manda E che ferma l'alphabot

    message = s.recv(BUFFER_SIZE)
    answer_server = message.decode()
    status, phrase = answer_server.split("|")
    print(f"Stato: {status}")
    print(f"Frase: {phrase}")

def heartbeat_receive():
    while True:
        data = heartbeat_socket.recv(BUFFER_SIZE)
        if not data:
            print("Connessione persa con il server!")
            break
        print("Heartbeat ricevuto")

def main():
    #thread per ascoltare l'heartbeat
    thread_heartbeat = threading.Thread(target=heartbeat_receive)
    thread_heartbeat.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()

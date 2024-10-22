from pynput import keyboard

pulsanti = {
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "e": False
}

def on_press(key):
    if key.char == "w" and not pulsanti["w"]:
        print("premuto w")
        pulsanti["w"] = True  
    elif key.char == "s" and not pulsanti["s"]:
        print("premuto s")
        pulsanti["s"] = True 
    elif key.char == "a" and not pulsanti["a"]:
        print("premuto a")
        pulsanti["a"] = True  
    elif key.char == "d" and not pulsanti["d"]:
        print("premuto d")
        pulsanti["d"] = True  
    elif key.char == "e" and not pulsanti["e"]:
        print("premuto e")
        pulsanti["e"] = True 


def on_release(key):
    if key.char == "w" and pulsanti["w"]:
        print("rilascito w")
        pulsanti["w"] = False  
    elif key.char == "s" and pulsanti["s"]:
        print("rilascito s")
        pulsanti["s"] = False  
    elif key.char == "a" and pulsanti["a"]:
        print("rilascito a")
        pulsanti["a"] = False  
    elif key.char == "d" and pulsanti["d"]:
        print("rilascito d")
        pulsanti["d"] = False  
    elif key.char == "e" and pulsanti["e"]:
        print("rilascito e")
        pulsanti["e"] = False  

'''
def on_press(key):
    if key.char in pulsanti and not pulsanti[key.char]:
        print(f"premuto {key.char}")
        pulsanti[key.char] = True  #segnala che il tasto è stato premuto


def on_release(key):
    if key.char in pulsanti and pulsanti[key.char]:
        print(f"rilascito {key.char}")
        pulsanti[key.char] = False  #segnala che il tasto è stato rilasciato
'''
'''
def on_press(key):
    if key.char == "w":
        print("premuto w")
    elif key.char == "s":
        print("premuto s")
    elif key.char == "a":
        print("premuto a")
    elif key.char == "d":
        print("premuto d")
    elif key.char == "e":
        print("premuto e")
    
    s.sendall(key.char.upper().encode()) 

   
def on_release(key):
    if key.char == "w":
        print("rilascito w")
    elif key.char == "s":
        print("rilascito s")
    elif key.char == "a":
        print("rilascito a")
    elif key.char == "d":
        print("rilascito d")
    elif key.char == "e":
        print("premuto e")
    
    s.sendall(key.char.upper().encode())
    #s.sendall("E".encode()) #per fermare quando rilascio i tasti
'''




def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()

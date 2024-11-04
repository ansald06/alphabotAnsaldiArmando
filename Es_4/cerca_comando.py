import sqlite3

#connesione al database
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()
command = "Q"
cur.execute(f"SELECT str_mov FROM comandi WHERE comando = '{command}'")
conn.commit()
variabie_in_stampa = cur.fetchone()
print(variabie_in_stampa)
    
str_mov = variabie_in_stampa[0] # Ottieni il primo elemento della prima tupla

# Ora puoi fare lo split della stringa
mov_list = str_mov.split(',')


for move in mov_list:
    direction = move[0]  #comando 
    duration = int(move[1:])  #tempo

    print(direction)
    print(duration)

conn.close()
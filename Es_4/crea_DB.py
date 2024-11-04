import sqlite3

#connesione al database
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE comandi (
                    comando VARCHAR(1),
                    str_mov TEXT NOT NULL,
                    PRIMARY KEY (comando)
            );
            ''')
conn.commit()
variabie_in_stampa = cur.fetchall()
#conn.close()


'''
    STRUTTURA DATABASE

PRIMARY KEY       STR_MOV
VARCHAR(1)         TEXT

    "A"         "F100,L40,F20"
    
'''
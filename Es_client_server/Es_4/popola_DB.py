import sqlite3

#connesione al database
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()

cur.execute('''
            INSERT INTO comandi
                (comando, str_mov)
            VALUES
                ("Q", "F100,L40,F20"),
                ("F", "F100,R40,F20");
            ''')
conn.commit()
variabie_in_stampa = cur.fetchall()
#conn.close()

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from AlphaBot import AlphaBot 

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Per la gestione della sessione

# Funzione per creare la tabella se non esiste
def create_table():
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    con.commit()
    con.close()

# Funzione per verificare le credenziali di login
def validate(username, password):
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    cur.execute("SELECT password FROM Users WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()
    if row:
        db_password = row[0]
        return db_password == password
    return False

# Funzione per inserire un nuovo utente nel database
def create_user(username, password):
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
    except sqlite3.IntegrityError:
        return False  # Ritorna False se l'utente esiste già
    finally:
        con.close()
    return True

@app.route("/")
def index():
    username = request.cookies.get('username')
    if username:
        return redirect(url_for('controllo'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        if validate(username, password):
            session['username'] = username  # Memorizziamo l'utente nella sessione
            response = redirect(url_for('controllo'))  # Reindirizza alla pagina di controllo Alphabot
            response.set_cookie('username', username, max_age=60 * 60 * 24, httponly=True)  # Cookie valido per 1 giorno
            return response
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        if create_user(username, password):
            success = "Account created successfully! You can now log in."
        else:
            error = "Username already exists. Please try a different one."
    return render_template('create_account.html', error=error, success=success)

@app.route('/controllo', methods=['GET', 'POST'])
def controllo():
    # Leggi il cookie per verificare l'utente
    username = request.cookies.get('username')
    
    bot = AlphaBot()

    # Se il cookie non esiste o non è valido, reindirizza alla pagina di login
    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'W':  # Avanti
            print("Bottone W - Avanti")
            bot.forward()
        elif action == 'A':  # Sinistra
            print("Bottone A - Sinistra")
            bot.left()
        elif action == 'S':  # Indietro
            print("Bottone S - Indietro")
            bot.backward()
        elif action == 'D':  # Destra
            print("Bottone D - Destra")
            bot.right()
        else:
            print("Unknown action")
            bot.stop()
    return render_template('controllo_alphabot.html', username=username)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Rimuove l'utente dalla sessione e cancella il cookie
    session.pop('username', None)
    response = redirect(url_for('login'))
    response.set_cookie('username', '', max_age=0)  # Rimuove il cookie impostandolo a scaduto
    return response


if __name__ == '__main__':
    create_table()  # Assicurati che la tabella venga creata
    app.run(debug=True)

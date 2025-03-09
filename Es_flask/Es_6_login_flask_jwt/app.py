from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import jwt
import datetime
from AlphaBot import AlphaBot  

app = Flask(__name__)
app.secret_key = 'supersecretkey'

SECRET_KEY = "mysecretkey"

bot = AlphaBot()

# Funzione per generare un token JWT
def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Per autenticare le richieste con JWT
@app.before_request
def authenticate():
    if 'Authorization' in request.headers:
        auth_header = request.headers.get('Authorization')
        if auth_header and " " in auth_header:
            try:
                token = auth_header.split(" ")[1]
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                session['username'] = decoded_token.get("username")
            except jwt.ExpiredSignatureError:
                session.pop('username', None)
            except jwt.InvalidTokenError:
                session.pop('username', None)

# Funzione per creare la tabella utenti
def create_table():
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    con.commit()
    con.close()

# Funzione per validare le credenziali
def validate(username, password):
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    cur.execute("SELECT password FROM Users WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()
    if row:
        return row[0] == password
    return False

# Funzione per creare un nuovo utente
def create_user(username, password):
    con = sqlite3.connect('./db_users.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
    except sqlite3.IntegrityError:
        return False  
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
            session['username'] = username  
            #token = generate_token(username)  
            response = redirect(url_for('controllo'))
            response.set_cookie('username', username, max_age=60 * 60 * 24, httponly=True)
            #response.set_cookie('token', token, max_age=60 * 60 * 24, httponly=True)
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

@app.route('/controllo', methods=['GET'])
def controllo():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('controllo_alphabot.html', username=username)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    action = data.get('action', '')

    if action == 'W':
        #print('W')
        bot.forward()  
    elif action == 'A':
        #print('A')
        bot.left()  
    elif action == 'S':
        #print('S')
        bot.backward()  
    elif action == 'D':
        #print('D')
        bot.right()   
    elif action == 'STOP':
        #print('STOP')
        bot.stop()  

    return jsonify({"status": "OK", "action": action})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    response = redirect(url_for('login'))
    response.set_cookie('username', '', max_age=0)
    response.set_cookie('token', '', max_age=0)
    return response

if __name__ == '__main__':
    create_table()  
    app.run(host='0.0.0.0', port=5000, debug=True)

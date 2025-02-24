from flask import Flask, render_template, request
from alphabot import AlphaBot  # Assicurati di importare il modulo dell'Alphabot

app = Flask(__name__)

# Inizializzazione dell'Alphabot
alphabot = AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'W':  # Avanti
            print("Bottone W - Avanti")
            alphabot.forward()
        elif action == 'A':  # Sinistra
            print("Bottone A - Sinistra")
            alphabot.left()
        elif action == 'S':  # Indietro
            print("Bottone S - Indietro")
            alphabot.backward()
        elif action == 'D':  # Destra
            print("Bottone D - Destra")
            alphabot.right()
        else:
            print("Unknown action")
            alphabot.stop()
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='localhost')

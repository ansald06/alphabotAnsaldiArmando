from flask import Flask, render_template, request

app = Flask(__name__)

# Inizializzazione dell'Alphabot
# alphabot = AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')  # Usa 'get' per evitare errori di chiave mancante
        if action == 'W':  # Avanti
            print("Bottone W - Avanti")
            # alphabot.forward()
        elif action == 'A':  # Sinistra
            print("Bottone A - Sinistra")
            # alphabot.left()
        elif action == 'S':  # Indietro
            print("Bottone S - Indietro")
            # alphabot.backward()
        elif action == 'D':  # Destra
            print("Bottone D - Destra")
            # alphabot.right()
        else:
            print("Unknown action")
            # alphabot.stop()
    return render_template('controllo_alphabot.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Porta diversa per evitare conflitti con app.py

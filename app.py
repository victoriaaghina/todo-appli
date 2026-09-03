from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('taches.db')
    taches = conn.execute('SELECT * FROM taches').fetchall()
    conn.close()
    return render_template('index.html', taches=taches)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    nouvelle_tache = request.form['tache']
    conn = sqlite3.connect('taches.db')
    conn.execute('INSERT INTO taches (description) VALUES (?)', (nouvelle_tache,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/cocher/<int:id>', methods=['POST'])
def cocher(id):
    conn = sqlite3.connect('taches.db')
    conn.execute('UPDATE taches SET fait = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
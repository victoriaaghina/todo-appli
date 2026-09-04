from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'oui'

@app.route('/')
def index():
    conn = sqlite3.connect('taches.db')
    taches = conn.execute('SELECT * FROM taches').fetchall()
    conn.close()
    pseudo_connecte = session.get('pseudo')
    return render_template('index.html', taches=taches, pseudo_connecte=pseudo_connecte)

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

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    conn = sqlite3.connect('taches.db')
    conn.execute('DELETE FROM taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/inscription', methods=['POST'])
def inscription():
    pseudo = request.form['pseudo']
    mot_de_passe = request.form['mot_de_passe']
    mot_de_passe_hache = generate_password_hash(mot_de_passe)
    conn = sqlite3.connect('taches.db')
    conn.execute('INSERT INTO users (pseudo, mot_de_passe) VALUES (?, ?)', (pseudo, mot_de_passe_hache))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/connexion', methods=['POST'])
def connexion():
    pseudo = request.form['pseudo']
    mot_de_passe = request.form['mot_de_passe']

    conn = sqlite3.connect('taches.db')
    utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (pseudo,)).fetchone()
    conn.close()

    if utilisateur and check_password_hash(utilisateur[2], mot_de_passe):
        session['pseudo'] = pseudo
        return redirect('/')
    else:
        return "Pseudo ou mot de passe incorrect"

@app.route('/deconnexion')
def deconnexion():
    session.pop('pseudo', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
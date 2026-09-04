from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'oui'

@app.route('/')
def index():
    conn = sqlite3.connect('taches.db')
    pseudo_connecte = session.get('pseudo')

    if pseudo_connecte:
        utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (pseudo_connecte,)).fetchone()
        mes_taches = conn.execute('SELECT * FROM taches WHERE id_user = ?', (utilisateur[0],)).fetchall()
        taches_partagees = conn.execute('''
            SELECT taches.*, users.pseudo AS utilisateur_partage FROM taches
            JOIN partages ON taches.id = partages.id_tache
            JOIN users ON taches.id_user = users.id
            WHERE partages.id_user = ?
        ''', (utilisateur[0],)).fetchall()
        tous_les_users = conn.execute('SELECT * FROM users WHERE id != ?', (utilisateur[0],)).fetchall()
    else:
        mes_taches = []
        taches_partagees = []
        tous_les_users = []

    conn.close()
    return render_template('index.html', mes_taches=mes_taches, taches_partagees=taches_partagees, pseudo_connecte=pseudo_connecte, tous_les_users=tous_les_users)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    if 'pseudo' not in session:
        return redirect('/')

    nouvelle_tache = request.form['tache']
    conn = sqlite3.connect('taches.db')
    utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (session['pseudo'],)).fetchone()
    conn.execute('INSERT INTO taches (description, id_user) VALUES (?, ?)', (nouvelle_tache, utilisateur[0]))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/cocher/<int:id>', methods=['POST'])
def cocher(id):
    if 'pseudo' not in session:
        return {'erreur': 'non connecté'}, 401

    conn = sqlite3.connect('taches.db')
    utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (session['pseudo'],)).fetchone()
    tache = conn.execute('SELECT * FROM taches WHERE id = ?', (id,)).fetchone()

    if tache is None:
        conn.close()
        return {'erreur': 'introuvable'}, 404

    est_proprietaire = tache[3] == utilisateur[0]
    partage = conn.execute('SELECT * FROM partages WHERE id_tache = ? AND id_user = ?', (id, utilisateur[0])).fetchone()
    a_acces_partage = partage is not None

    if not est_proprietaire and not a_acces_partage:
        conn.close()
        return {'erreur': 'non autorisé'}, 403

    nouvel_etat = 0 if tache[2] else 1 #le bouton inverse l'état de la tache (si elle était faite alors elle ne l'est plus et inversement)
    conn.execute('UPDATE taches SET fait = ? WHERE id = ?', (nouvel_etat, id))
    conn.commit()
    conn.close()
    return {'fait': nouvel_etat}

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    if 'pseudo' not in session:
        return redirect('/')

    conn = sqlite3.connect('taches.db')
    utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (session['pseudo'],)).fetchone()
    tache = conn.execute('SELECT * FROM taches WHERE id = ?', (id,)).fetchone()

    if tache is None or tache[3] != utilisateur[0]:
        conn.close()
        return redirect('/')

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

@app.route('/partager', methods=['POST'])
def partager():
    if 'pseudo' not in session:
        return redirect('/')

    id_tache = request.form['id_tache']
    id_user_cible = request.form['id_user_cible']

    conn = sqlite3.connect('taches.db')
    utilisateur = conn.execute('SELECT * FROM users WHERE pseudo = ?', (session['pseudo'],)).fetchone()
    tache = conn.execute('SELECT * FROM taches WHERE id = ?', (id_tache,)).fetchone()

    if tache is None or tache[3] != utilisateur[0]:
        conn.close()
        return redirect('/')

    conn.execute('INSERT INTO partages (id_user, id_tache) VALUES (?, ?)', (id_user_cible, id_tache))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
import sqlite3

conn = sqlite3.connect('taches.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL
    )
''')
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL UNIQUE,
        mot_de_passe TEXT NOT NULL
    )
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS partages (
        id_user INTEGER NOT NULL,
        id_tache INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id),
        FOREIGN KEY (id_tache) REFERENCES taches(id)
    )
''')

conn.commit()
conn.close()

print("Base de données initialisée.")
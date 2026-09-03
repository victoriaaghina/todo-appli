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
conn.commit()
conn.close()

print("Base de données initialisée.")
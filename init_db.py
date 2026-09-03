import sqlite3

conn = sqlite3.connect('taches.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

print("Base de données initialisée.")
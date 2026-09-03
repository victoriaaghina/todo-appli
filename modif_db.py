import sqlite3

conn = sqlite3.connect('taches.db')
conn.execute('ALTER TABLE taches ADD COLUMN fait INTEGER NOT NULL DEFAULT 0')
conn.commit()
conn.close()

print("Colonne 'fait' ajoutée.")
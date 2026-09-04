import sqlite3

conn = sqlite3.connect('taches.db')
conn.execute('ALTER TABLE taches ADD COLUMN id_user INTEGER')
conn.commit()
conn.close()

print("Colonne 'id_user' ajoutée.")
from unidecode import unidecode
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('../db.db')
cursor = conn.cursor()

# Update existing data
cursor.execute("SELECT player_id, name FROM players")
rows = cursor.fetchall()

for player_id, name in rows:
    name_unaccented = unidecode(name)
    cursor.execute("UPDATE players SET name_unaccented = ? WHERE player_id = ?", (name_unaccented, player_id))

conn.commit()
conn.close()

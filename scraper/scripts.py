from unidecode import unidecode
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('../db.db')
cursor = conn.cursor()

def add_unaccented():
    # Update existing data
    cursor.execute("SELECT player_id, name FROM players")
    rows = cursor.fetchall()

    for player_id, name in rows:
        name_unaccented = unidecode(name)
        cursor.execute("UPDATE players SET name_unaccented = ? WHERE player_id = ?", (name_unaccented, player_id))

def update_league_id():
    cursor.execute("SELECT * FROM leagues")
    rows = cursor.fetchall()
    for _, _, ref, _ in rows:
        league_id = f"{ref.split('/')[1].replace('-', '_')}_{ref.split('/')[-1].replace('-', '_')}"
        cursor.execute("UPDATE leagues SET league_id = ? WHERE ref = ?", (league_id, ref))

update_league_id()
conn.commit()
conn.close()

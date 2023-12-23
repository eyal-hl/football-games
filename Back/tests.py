import sqlite3
from tabulate import tabulate
from const import DB_PATH

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

table_names = ["hapoel_hadera", "hapoel_haifa", "maccabi_haifa"]
columns = ", ".join([f"max(t{index + 1}.year) as {table}_year" for index, table in enumerate(table_names)])

query = f'''
    SELECT t1.player_id, t1.player_name, {columns}
    FROM {table_names[0]} t1
    INNER JOIN {table_names[1]} t2 ON t1.player_id = t2.player_id
    INNER JOIN {table_names[2]} t3 ON t1.player_id = t3.player_id
    GROUP BY t1.player_id;
'''
result = c.execute(query)

# Fetch all rows
rows = result.fetchall()

# Get the column names
column_names = [description[0] for description in result.description]

# Convert the rows and column names to a table and print it
table = tabulate(rows, headers=column_names)
print(f"All players that played in {table_names[0]}, {table_names[1]}, {table_names[2]} are:")
print(table)

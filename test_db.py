import sqlite3

# abre conexão com o mesmo arquivo que o DB Browser usa
conn = sqlite3.connect("data/seguros.db")
cur = conn.cursor()

cur.execute("SELECT * FROM clientes;")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()

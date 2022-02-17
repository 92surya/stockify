import psycopg2
import os

conn = psycopg2.connect(database="stocks",
                        user='postgres', password='Netradyne123',
                        host='localhost', port='5432'
                        )

cur = conn.cursor()
with open("migrations.sql", 'r') as f:
    cur.execute(f.read())
conn.commit()
print("created tables!")

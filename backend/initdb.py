import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO cards (title, pinyin, content) VALUES (?, ?, ?)",
            ('怎', "zěn",'Content for the first post')
            )
cur.execute("INSERT INTO cards (title, pinyin, content) VALUES (?, ?, ?)",
            ('书', "shū",'Content for the first post')
            )
cur.execute("INSERT INTO cards (title, pinyin, content) VALUES (?, ?, ?)",
            ('馆', "guǎn",'Content for the first post')
            )
connection.commit()
connection.close()
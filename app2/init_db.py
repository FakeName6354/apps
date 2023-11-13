import sqlite3

connection = sqlite3.connect('database.db')


f = open('schema.sql')
connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
            ('testuser', '123456', 'test_user_name')
            )

cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
            ('user', '123456', 'test_user_name')
            )

cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
            ('user2', '123456', 'test_user_name')
            )


connection.commit()
connection.close()

f.close();

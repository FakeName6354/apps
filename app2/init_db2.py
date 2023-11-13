import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="database",
    user="postgres",
    password="postgres"
)

#cur = connection.cursor()

f = open('schema.sql')
connection.execute(f.read())

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

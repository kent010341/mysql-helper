from mysqlhelper import db_connector

config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "database": "my_taable"
}

@db_connector(**config)
def demo(cursor):
    cursor.execute("SELECT name FROM my_table LIMIT 1")
    return cursor.fetchall()

print(demo())

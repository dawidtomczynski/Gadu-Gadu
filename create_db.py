import psycopg2

sql_create_db = "CREATE DATABASE GaduGadu;"
sql_create_table_users = "CREATE TABLE Users(" \
                         "id serial NOT NULL PRIMARY KEY, " \
                         "username varchar(255) NOT NULL, " \
                         "hashed_password varchar(80) NOT NULL)"
sql_create_table_messages = "CREATE TABLE Messages(" \
                         "id serial NOT NULL PRIMARY KEY," \
                         "from_id int NOT NULL," \
                         "to_id int NOT NULL," \
                         "creation_date timestamp NOT NULL," \
                         "text varchar(255) NOT NULL," \
                         "FOREIGN KEY (from_id) REFERENCES Users(id)," \
                         "FOREIGN KEY (to_id) REFERENCES Users(id))"

try:
    connection = psycopg2.connect(
        user="postgres", password="123Frytki",
        host="127.0.0.1", port="5432"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(sql_create_db)
        print("Database created.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists.")
    connection.close()

    connection = psycopg2.connect(
        database="gadugadu", user="postgres", password="123Frytki",
        host="127.0.0.1", port="5432"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(sql_create_table_users)
        print("Table created.")
    except psycopg2.errors.DuplicateTable:
        print("Table already exists.")
    try:
        cursor.execute(sql_create_table_messages)
        print("Table created.")
    except psycopg2.errors.DuplicateTable:
        print("Table already exists.")
    connection.close()
except psycopg2.errors.OperationalError:
    print("Problem connecting to the server.")

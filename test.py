from models import Users
import psycopg2

connection = psycopg2.connect(
    database="gadugadu", user="postgres",
    password="123Frytki", host="127.0.0.1",
)
connection.autocommit = True
cursor = connection.cursor()

# new_user = Users('biwak', 'zelazko')
# new_user.save_to_db(cursor)

# x = Users.load_user_by_id(cursor, 1)
# x.hashed_password = 'hakuna'
# x.save_to_db(cursor)

# y = Users.load_user_by_id(cursor, 2)
# y.delete(cursor)

print(Users.load_user_by_id(cursor, 1))
# print(Users.load_user_by_id(cursor, 5))

# print(Users.load_all_users(cursor))

connection.close()

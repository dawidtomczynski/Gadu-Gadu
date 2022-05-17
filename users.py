import psycopg2
from models import Users
from clcrypto import check_password

connection = psycopg2.connect(
    database="gadugadu", user="postgres",
    password="123Frytki", host="127.0.0.1",
)
connection.autocommit = True
cursor = connection.cursor()


def new_user(username, password):
    x = Users(username, password)
    try:
        x.save_to_db(cursor)
        print("User added.")
    except psycopg2.errors.UniqueViolation:
        print("User already exists.")


def change_password(username, password, new_password):
    x = Users.load_user_by_username(cursor, username)
    hashed_password = x.hashed_password
    checked_password = check_password(password, hashed_password)
    if checked_password:
        x.hashed_password = new_password
        x.save_to_db(cursor)
        print("Password changed.")
    else:
        print("Incorrect password.")


def del_user(username, password):
    x = Users.load_user_by_username(cursor, username)
    hashed_password = x.hashed_password
    checked_password = check_password(password, hashed_password)
    if checked_password:
        x.delete(cursor)
        print("User deleted.")
    else:
        print("Incorrect password.")


def user_input():
    print("1. Add new user \n2. Edit password \n3. Delete user \n4. List all users \n5. End program \n")
    option = input("Choose an option: ")
    if option == "1":
        while True:
            username = input("Username: ")
            password = input("Password (min. 8 characters): ")
            if len(password) < 8:
                print("Password too short.\n")
            else:
                new_user(username, password)
                return False
    if option == "2":
        username = input("Username: ")
        password = input("Old password: ")
        new_password = input("New password: ")
        while True:
            if len(new_password) < 8:
                print("Password too short.\n")
            else:
                change_password(username, password, new_password)
                return False
    if option == "3":
        username = input("Username: ")
        password = input("Password: ")
        return del_user(username, password)
    if option == "4":
        print(Users.load_all_users(cursor))


user_input()

connection.close()

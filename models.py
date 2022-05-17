from clcrypto import hash_password
from datetime import datetime


class Users:
    def __init__(self, username="", password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO Users(username, hashed_password) VALUES (%s, %s) RETURNING id"
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE Users SET username=%s, hashed_password=%s WHERE id=%s"
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM Users WHERE username=%s"
        cursor.execute(sql, (username, ))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM Users WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = Users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

    def __repr__(self):
        return f"ID: {self._id}, Username: {self.username}, Password: {self._hashed_password} \n"


class Messages:
    def __init__(self, from_id="", to_id="", text="" , creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        now = datetime.now()
        if self._id == -1:
            sql = "INSERT INTO Messages(from_id, to_id, text, creation_date) VALUES (%s, %s, %s, %s) RETURNING id"
            values = (self.from_id, self.to_id, self.text, now)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE Messages SET from_id=%s, to_id=%s, text=%s, datetime=%s WHERE id=%s"
            values = (self.from_id, self.to_id, self.text, now, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Messages()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = text
            loaded_message.creation_date = creation_date
            messages.append(loaded_message)
            return messages

    @staticmethod
    def load_messages_by_to_id(cursor, to_id):
        sql = "SELECT id, username, hashed_password FROM Users WHERE id=%s"
        cursor.execute(sql, (to_id,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user


    def __repr__(self):
        return f"From ID: {self.from_id}, To ID: {self.to_id}, Message: {self.text}, Date: {self.creation_date} \n"

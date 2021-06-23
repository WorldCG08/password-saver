import os
import sqlite3
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import uuid
import pyclip
from .login import Login


def help_menu():
    print('''------COMMANDS------\ns - search\nsr - Speech recognition (Search with you microphone)
c - copy password by ID\na - add login\nd - delete login\nall - show all
help - to show this commands again\nuuid-show - show uuid (dont share this key!!!)
ctrl + D - to quit\n--------------------''')


def hw_salt():
    if os.path.exists('.' + os.sep + 'ferkey.txt'):
        with open('ferkey.txt', 'r') as f:
            st = f.readline().strip().encode()
    else:
        st = str(uuid.getnode()).encode()  # set generated UUID from comman uuid-show HERE!!!!
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(st))


def _encrypt(password):
    fernet = Fernet(hw_salt())
    return fernet.encrypt(password.encode()).decode()


def _decrypt(password):
    fernet = Fernet(hw_salt())
    return fernet.decrypt(password.encode()).decode()


class Controller:
    """Controller for database"""

    def __init__(self):

        if os.path.exists('.' + os.sep + 'ddb.db'):
            self.connection = sqlite3.connect('ddb.db')
        else:
            self.connection = sqlite3.connect('ddb.db')
            cur = self.connection.cursor()
            cur.execute('''CREATE TABLE logins (id INTEGER	constraint persons_pk primary key autoincrement,
             login text, password text, description text)''')

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def save(self, login_entity: Login):
        """Put login object to save to database"""

        password = _encrypt(login_entity.password)
        self.cursor.execute(f"INSERT INTO logins (login, password, description) VALUES ('{login_entity.login}','{password}', '{login_entity.description}')")
        # Save (commit) the changes
        self.connection.commit()

    def delete(self, login_id):
        """remove login object from database"""

        self.cursor.execute(f"DELETE FROM logins WHERE id={login_id}")
        self.connection.commit()

    def search(self, search):
        self._person_formatter(f"SELECT * from logins where login LIKE '%{search}%' OR description LIKE '%{search}%'")

    def show_all(self):
        """Show all logins"""
        self._person_formatter()

    def show_uuid(self):
        print('WARNING!!! Don\'t share this key with anyone!!!')
        print(uuid.getnode())

    def get_password(self, login_id):
        cur = self.cursor
        for row in cur.execute('SELECT password FROM logins where id=:log_id', {"log_id": login_id}):
            pyclip.copy(_decrypt(row[0]))

    def _person_formatter(self, query_string="select * from logins"):
        """Formats output to one format"""

        cur = self.cursor

        print('{0:<6}'.format('ID'), end=' ')
        print('{0:20}'.format('Login'), end=' ')
        print('{0:200}'.format('Description'))
        for row in cur.execute(query_string):
            print('{0:<6}'.format(row[0]), end=' ')
            print('{0:20}'.format(row[1]), end=' ')
            print('{0:200}'.format(row[3]), end=' ')
            print()

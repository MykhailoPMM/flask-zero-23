import math
import time
import sqlite3
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Помилка зчитування інформації з БД')
        return []

    def add_post(self, title, text, url):
        try:
            self.__cur.execute(f'SELECT COUNT() as `count` FROM posts WHERE url LIKE \'{url}\'')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Стаття з таким url уже існує.')
                return False

            base = url_for('static', filename='images')
            text = re.sub(r'(?P<tag><img\s+[^>]*src=)(?P<quote>[\"])(?P<url>.+?)(?P=quote)>',
                          '\\g<tag>' + base + '/\\g<url>>', text)

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES (NULL, ?, ?, ?, ?)', (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as err:
            print('Помилка при додаванні статті в БД: ' + str(err))
            return False

        return True

    def get_post(self, alias):
        try:
            self.__cur.execute(f'SELECT title, text FROM posts WHERE url = \'{alias}\' LIMIT 1')
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as err:
            print('Помилка при отриманні статті з БД: ' + str(err))

        return (False, False)

    def get_posts(self):
        try:
            self.__cur.execute('SELECT title, text, url FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as err:
            print('Помилка при отриманні статтей з БД: ' + str(err))

        return []

    def add_user(self, name, email, hash_psw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Користувач з таким email уже існує.')
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (name, email, hash_psw, tm))
            self.__db.commit()
        except sqlite3.Error as err:
            print('Помилка запису користувача в БД!' + str(err))
            return False

        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone
            if not res:
                print('Користувач не знайдений.')
                return False

            return res
        except sqlite3.Error as err:
            print('Помилка при отриманні даних з БД: ' + str(err))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Користувач не знайдений.')
                return False

            return res
        except sqlite3.Error as err:
            print('Помилка при отриманні даних з БД: ' + str(err))

        return False

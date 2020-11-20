import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()


user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/create-user', methods=['POST'])
def create_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        conn.commit()
        cursor = conn.cursor()
        query = "INSERT INTO BankUser(UserId, CreatedAt, ModifiedAt) VALUES(?,datetime('now'),datetime('now'))"
        user = request.json
        try:
            cursor.execute(query, (user['UserId'],))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/get-user/<UserId>', methods=['GET'])
def get_user(UserId):
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM BankUser WHERE Id = ?"
            cursor = conn.cursor()
            user = request.json
            try:
                cursor.execute(query, (UserId, ))
                data = cursor.fetchone()
                if data:
                    return {'user': data}, 200
                else:
                    return {'status': "user not found"}, 300
            except sqlite3.Error as e:
                return str(e), 500

@user_controller.route('/api/get-all-users', methods=['GET'])
def get_all_users():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM BankUser"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'users': data }, 200
            else:
                return {'status': 'No data found' }, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/update-user', methods=['PUT'])
def update_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        queryUserTable = "UPDATE BankUser SET UserId = ?, ModifiedAt = datetime('now') WHERE Id = ?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(queryUserTable, (user["UserId"], user["BankUserId"] ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/delete-user/<userId>', methods=['DELETE'])
def delete_user(userId):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        query1 = "DELETE FROM BankUser WHERE Id=?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(query1, (userId, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()


user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/create-user', methods=['POST'])
def create_user():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO BorgerUser(UserId, CreatedAt) VALUES(?,datetime('now'))"
        user = request.json

        try:
            cursor.execute(query, (user['UserId'],))
            conn.commit()
            return {'status': 'success'}, 201
        except sqlite3.Error as e:
            return str(e), 400

@user_controller.route('/api/get-user/<UserId>', methods=['GET'])
def get_user(UserId):
        with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
            query = "SELECT * FROM BorgerUser WHERE Id = ?"
            cursor = conn.cursor()
            user = request.json
            try:
                cursor.execute(query, (UserId, ))
                data = cursor.fetchone()
                if data:
                    return {'user': data}, 200
                else:
                    return {'user': 'user not found'}, 404
            except sqlite3.Error as e:
                return str(e), 400

@user_controller.route('/api/get-all-users', methods=['GET'])
def get_all_users():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        query = "SELECT * FROM BorgerUser"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'users': data }, 200
        except sqlite3.Error as e:
            return str(e), 400

@user_controller.route('/api/update-user', methods=['PUT'])
def update_user():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        queryUserTable = "UPDATE BorgerUser SET UserId = ?, CreatedAt = datetime('now') WHERE Id = ?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(queryUserTable, (user["UserId"], user["BorgerUserId"] ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 400

@user_controller.route('/api/delete-user/<userId>', methods=['DELETE'])
def delete_user(userId):
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        query1 = "DELETE FROM BorgerUser WHERE Id=?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(query1, (userId, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 400
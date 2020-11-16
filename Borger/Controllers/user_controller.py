import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()


user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/createUser', methods=['POST'])
def create_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO BorgerUser(UserId, CreatedAt) VALUES(?,datetime('now'))"
        user = request.json
        try:
            cursor.execute(query, (user['UserId'],))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/getUser', methods=['GET'])
def get_user():
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM BorgerUser WHERE Id = ?"
            cursor = conn.cursor()
            user = request.json
            try:
                cursor.execute(query, (user["Id"], ))
                conn.commit()
                data = cursor.fetchall()
                return {'status': 'success', 'data': data }, 200
            except sqlite3.Error as e:
                return str(e), 500

@user_controller.route('/api/getAllUsers', methods=['GET'])
def get_all_users():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM BorgerUser"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'data': data }, 200
        except sqlite3.Error as e:
            return str(e), 500
        
@user_controller.route('/api/updateUser', methods=['PATCH'])
def update_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query1 = "UPDATE BorgerUser SET UserId = ?, CreatedAt = datetime('now')"
        cursor = conn.cursor()
        user = request.json
        # TO DO: update in Address table 
        try:
            cursor.execute(query1, (user["Id"], ))
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'data': data }, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/deleteUser', methods=['DELETE'])
def delete_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query1 = "DELETE FROM BorgerUser WHERE Id=?"
        query2 = "DELETE FROM Address WHERE BorgerUserId=?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(query1, (user["Id"], ))
            conn.commit()
            cursor.execute(query2, (user["Id"], ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500
import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/create-user', methods=['POST'])
def create_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO SkatUser(UserId, CreatedAt, IsActive) VALUES(?,datetime('now'), 'True')"
        user = request.json
        
        try:
            cursor.execute(query, (user['UserId'], ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500
        
@user_controller.route('/api/get-user/<Id>', methods=['GET'])
def get_user(Id):
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM SkatUser WHERE Id = ?"
            cursor = conn.cursor()
            user = request.json
            try:
                cursor.execute(query, (Id, ))
                data = cursor.fetchone()
                if data:
                    return {'Skat User': data}, 200
                else:
                    return {'Skat User': 'user not found'}, 200
            except sqlite3.Error as e:
                return str(e), 500

@user_controller.route('/api/get-all-users', methods=['GET'])
def get_all_users():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM SkatUser"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'users': data }, 200
        except sqlite3.Error as e:
            return str(e), 500

@user_controller.route('/api/update-user/<Id>', methods=['PUT'])
def update_user(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        queryUserTable = "UPDATE SkatUser SET UserId = ?, IsActive = ? WHERE Id = ? "
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(queryUserTable, (user["UserId"], user["IsActive"], Id ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 500
        
@user_controller.route('/api/delete-user/<Id>', methods=['DELETE'])
def delete_user(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "DELETE FROM SkatUser WHERE Id=?"
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(query, (Id, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
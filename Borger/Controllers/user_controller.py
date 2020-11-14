import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()


user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/createUser', methods=['POST'])
def create_user():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        cur = conn.cursor()
        query = "INSERT INTO BorgerUser(UserId, CreatedAt) VALUES(?,datetime('now'))"
        user = request.json
        try:
            cur.execute(query, (user['UserId'],))
            conn.commit()
            return 'success'
        except sqlite3.Error as e:
            return str(e), 400

@user_controller.route('/api/getUser', methods=['GET'])
def get_user():
    return 'it works!'

@user_controller.route('/api/getAllUsers', methods=['GET'])
def get_all_users():
    return 'it works!'

@user_controller.route('/api/updateUser', methods=['PATCH'])
def update_user():
    return 'it works!'

@user_controller.route('/api/deleteUser', methods=['DELETE'])
def delete_user():
    return 'it works!'
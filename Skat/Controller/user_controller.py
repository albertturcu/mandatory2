import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
import requests
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
            return {'status': str(e)}, 500
        
@user_controller.route('/api/get-user/<Id>', methods=['GET'])
def get_user(Id):
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM SkatUser WHERE Id = ?"
            cursor = conn.cursor()
            try:
                cursor.execute(query, (Id, ))
                data = cursor.fetchone()
                if data:
                    return {'Skat User': data}, 200
                else:
                    return {'Skat User': 'user not found'}, 200
            except sqlite3.Error as e:
                return {'status': str(e)}, 500

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
            return {'status': str(e)}, 500

@user_controller.route('/api/update-user/<Id>', methods=['PUT'])
def update_user(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "UPDATE SkatUser SET UserId = ?, IsActive = ? WHERE Id = ? "
        cursor = conn.cursor()
        user = request.json
        try:
            cursor.execute(query, (user["UserId"], user["IsActive"], Id ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
        
@user_controller.route('/api/delete-user/<Id>', methods=['DELETE'])
def delete_user(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "DELETE FROM SkatUser WHERE Id=?"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (Id, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

headers = {
    'Content-Type': 'application/json-patch+json'
}

@user_controller.route('/api/pay-taxes', methods=['POST'])
def pay_taxes():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        req_data = request.json
        query_get_user = "SELECT * FROM SkatUserYear WHERE UserId = ? "
        query_update_user = "UPDATE SkatUserYear SET Amount = ?, IsPaid = ? WHERE UserId = ? "
        cursor = conn.cursor()
        try:
            cursor.execute(query_get_user, (req_data['UserId'], ))
            conn.commit()
            user_data = cursor.fetchall()
            r_tax_calculator = requests.post('http://localhost:7071/api/Skat_Tax_Calculator', json={"money": req_data['Amount']}, headers=headers )
            r_withdraw_money = requests.post("http://localhost:5005/api/withdraw-money", json={"UserId": user_data[0][3], "Amount": r_tax_calculator.text }, headers=headers )
            print(r_withdraw_money.status_code)
            if int(user_data[0][4]) <= 0 and r_tax_calculator.status_code == 200 and r_withdraw_money.status_code == 200:
                    cursor.execute(query_update_user, ( r_tax_calculator.text, 1, user_data[0][3] ))
                    conn.commit()
                    return {'status': 'success'}, 200
            elif r_withdraw_money.status_code == 500:
                return {'status': 'Not enough money in your account'}, 404
            else:
                 return {'status': 'something went wrong'}, 404
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
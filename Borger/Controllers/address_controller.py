from flask import Blueprint, request
import sqlite3
from os import environ
from dotenv import load_dotenv
load_dotenv()


address_controller = Blueprint('address_controller', __name__)

@address_controller.route('/api/createAddress', methods=['POST'])
def create_address():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(?, ?, datetime('now'), True)"
        address = request.json
        try:
            cursor.execute("SELECT * FROM BorgerUser WHERE Id = ?", (address['BorgerUserId'], ))
            isUserRegistered = cursor.fetchone()
            cursor.execute("SELECT * FROM Address WHERE BorgerUserId = ?", (address['BorgerUserId'], ))
            isAddressRegistered = cursor.fetchall()

            if isUserRegistered and not isAddressRegistered:
                cursor.execute(query, (address['BorgerUserId'], address['Address']))
                conn.commit()
                return {'status': 'success'}, 200
            else:
                return {'status': 'The user id does not exist or the user has an active address already'}, 500
        except sqlite3.Error as e:
            return {'status': str(e)}, 500


@address_controller.route('/api/getAddress/<addressId>', methods=['GET'])
def get_address(addressId):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM Address WHERE Id = ?"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (addressId, ))
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'data': data}, 200
            else:
                return {'status': 'Not found'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

@address_controller.route('/api/getAllAddresses', methods=['GET'])
def get_all_addresss():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM Address"
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'data': data}, 200
            else:
                return {'status': 'Not found'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

@address_controller.route('/api/updateAddress', methods=['PUT'])
def update_address():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query1 = "UPDATE Address SET IsValid = False WHERE BorgerUserId = ?"
        query2 = "INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(?, ?, datetime('now'), True)"
        cursor = conn.cursor()
        address = request.json
        try:
            cursor.execute(query1, (address["BorgerUserId"], ))
            cursor.execute(query2, (address["BorgerUserId"], address["Address"], ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

@address_controller.route('/api/deleteAddress/<userId>', methods=['DELETE'])
def delete_address(userId):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query1 = "DELETE FROM BorgerUser WHERE Id=?"
        query2 = "DELETE FROM Address WHERE BorgerUserId=?"
        cursor = conn.cursor()
        try:
            cursor.execute(query1, (userId, ))
            cursor.execute(query2, (userId, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

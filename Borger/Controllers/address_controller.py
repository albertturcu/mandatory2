from flask import Blueprint, request
import sqlite3
from os import environ
from dotenv import load_dotenv
load_dotenv()


address_controller = Blueprint('address_controller', __name__)

@address_controller.route('/api/create-address', methods=['POST'])
def create_address():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        query = "INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(?, ?, datetime('now'), True)"
        address = request.json
        try:
            cursor.execute("SELECT * FROM Address WHERE BorgerUserId = ?", (address['BorgerUserId'], ))
            isAddressRegistered = cursor.fetchall()

            if not isAddressRegistered:
                cursor.execute(query, (address['BorgerUserId'], address['Address']))
                conn.commit()
                return {'status': 'success'}, 201
            else:
                return {'status': 'The user id does not exist or the user has an active address already'}, 404
        except sqlite3.Error as e:
            return {'status': str(e)}, 400


@address_controller.route('/api/get-address/<addressId>', methods=['GET'])
def get_address(addressId):
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        query = "SELECT * FROM Address WHERE Id = ?"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (addressId, ))
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'data': data}, 200
            else:
                return {'status': 'Not found'}, 404
        except sqlite3.Error as e:
            return {'status': str(e)}, 400

@address_controller.route('/api/get-all-addresses', methods=['GET'])
def get_all_addresss():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        query = "SELECT * FROM Address"
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'data': data}, 200
            else:
                return {'status': 'Address not found'}, 404
        except sqlite3.Error as e:
            return {'status': str(e)}, 400

@address_controller.route('/api/update-address', methods=['PUT'])
def update_address():
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
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
            return {'status': str(e)}, 400

@address_controller.route('/api/delete-address/<userId>', methods=['DELETE'])
def delete_address(userId):
    with sqlite3.connect("borger.sqlite", check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        query2 = "DELETE FROM Address WHERE BorgerUserId=?"
        cursor = conn.cursor()
        try:
            cursor.execute(query2, (userId, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 400

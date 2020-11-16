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
        # query = "INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(? , ?,datetime('now'), True ) WHERE NOT EXISTS (SELECT * FROM Address WHERE BorgerUserId =? AND IsValid = True)"
        query = "If NOT EXISTS(SELECT * FROM Address WHERE BorgerUserId =? AND IsValid = True) INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(? , ?,datetime('now'), True ) "
        address = request.json
        try:
            cursor.execute("SELECT Id FROM BorgerUser WHERE Id = ?", (address['BorgerUserId'], ))
            result1 = cursor.fetchone()
            cursor.execute("SELECT IsValid FROM Address WHERE BorgerUserId = ?", (address['BorgerUserId'], ))
            result2 = cursor.fetchall()
            # TO DO: check if the user has an active address already
            if result1 != None and len(result2) !=0:
                cursor.execute(query, (address['BorgerUserId'], address['Address'], address['BorgerUserId'] ))
                conn.commit()
                return {'status': 'success'}, 200
            else:
                return "The user id does not exist or the user has an active address already", 500
        except sqlite3.Error as e:
            return str(e), 500


@address_controller.route('/api/getAddress', methods=['GET'])
def get_address():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM Address WHERE Id = ?"
            cursor = conn.cursor()
            address = request.json
            try:
                cursor.execute(query, (address["Id"], ))
                conn.commit()
                data = cursor.fetchall()
                return {'status': 'success', 'data': data }, 200
            except sqlite3.Error as e:
                return str(e), 500

@address_controller.route('/api/getAllAddresss', methods=['GET'])
def get_all_addresss():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM Address"
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'data': data }, 200
        except sqlite3.Error as e:
            return str(e), 500

@address_controller.route('/api/updateAddress', methods=['PATCH'])
def update_address():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query1 = "UPDATE Address SET IsValid = False WHERE BorgerUserId = ?"
        query2 = "INSERT INTO Address(BorgerUserId, Address, CreatedAt, IsValid) VALUES(? , ?,datetime('now'), True)"
        cursor = conn.cursor()
        address = request.json
        print(address)
        try:
            cursor.execute(query1, (address["BorgerUserId"], ))
            cursor.execute(query2, (address["BorgerUserId"], address["Address"], ))
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'data': data }, 200
        except sqlite3.Error as e:
            return str(e), 500
    return 'it works!'

@address_controller.route('/api/deleteAddress', methods=['DELETE'])
def delete_address():
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query1 = "DELETE FROM BorgerUser WHERE Id=?"
            query2 = "DELETE FROM Address WHERE Id=?"
            cursor = conn.cursor()
            user = request.json
            try:
                cursor.execute(query1, (user["Id"], ))
                cursor.execute(query2, (user["Id"], ))
                conn.commit()
                return {'status': 'success'}, 200
            except sqlite3.Error as e:
                return str(e), 500
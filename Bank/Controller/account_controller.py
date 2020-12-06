import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
import os
load_dotenv()


account_controller = Blueprint('account_controller', __name__)

@account_controller.route('/api/create-account', methods=['POST'])
def create_account():
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        query = "INSERT INTO Account(BankUserId, AccountNo, IsStudent, CreatedAt, ModifiedAt, Amount) VALUES(?,?,?,datetime('now'),datetime('now'),?)"
        account = request.json
        try:
            cursor.execute(query, (account['BankUserId'],account['AccountNo'],account['IsStudent'],account['Amount']))
            conn.commit()
            return {'status': 'success'}, 201
        except sqlite3.Error as e:
            return str(e), 500

@account_controller.route('/api/get-account/<AccountId>', methods=['GET'])
def get_account(AccountId):
        with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
            query = "SELECT * FROM Account WHERE Id = ?"
            cursor = conn.cursor()
            try:
                cursor.execute(query, (AccountId, ))
                data = cursor.fetchone()
                if data:
                    return {'account': data}, 200
                else:
                    return {'status': "account not found"}, 404
            except sqlite3.Error as e:
                return str(e), 400

@account_controller.route('/api/get-all-accounts', methods=['GET'])
def get_all_accounts():
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        query = "SELECT * FROM Account"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            if data:
                return {'status': 'success', 'accounts': data }, 200
            else:
                return {'status': 'No data found' }, 404
        except sqlite3.Error as e:
            return str(e), 400

@account_controller.route('/api/update-account', methods=['PUT'])
def update_account():
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        queryAccountTable = "UPDATE Account SET IsStudent = ?, Amount = ?, ModifiedAt = datetime('now') WHERE BankUserId = ?"
        cursor = conn.cursor()
        account = request.json
        try:
            cursor.execute(queryAccountTable, (account['IsStudent'],account['Amount'], account['BankUserId']))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return str(e), 400

@account_controller.route('/api/delete-account/<AccountId>', methods=['DELETE'])
def delete_account(AccountId):
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        query1 = "DELETE FROM Account WHERE Id=?"
        cursor = conn.cursor()
        try:
            cursor.execute(query1, (AccountId, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 404

@account_controller.route('/api/withdraw-money', methods=['POST'])
def wtihdraw_money():
    data = request.json
    selectBankUserIdQuery = "SELECT Id FROM BankUser WHERE UserId=?"
    selectAmountForBankUserIdQuery = "SELECT Amount FROM Account WHERE BankUserId = ?"
    updateAmountForBankUserIdQuery = "UPDATE Account SET Amount = ? WHERE BankUserId = ?"

    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(selectBankUserIdQuery, (data['UserId'],))
            bankUserId = cursor.fetchone()
            if bankUserId:
                bankUserId = bankUserId[0]
            else:
                raise Exception("Account not found!")
            cursor.execute(selectAmountForBankUserIdQuery, (bankUserId,))
            currentAccountAmount = cursor.fetchone()[0]
            if currentAccountAmount - data['Amount'] >= 0:
                newAccountAmount = currentAccountAmount - data['Amount']
                cursor.execute(updateAmountForBankUserIdQuery, (newAccountAmount, bankUserId))
                conn.commit()
                return {'status': 'Success withdraw'}, 200
            else:
                return {'status': 'Not enough money'}, 404
        except sqlite3.Error as e:
            return {'status': str(e)}, 400
        except Exception as e:
            return {'status': str(e)}, 400
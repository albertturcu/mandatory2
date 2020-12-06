import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
import requests
load_dotenv()


deposit_controller = Blueprint('deposit_controller', __name__)
headers = {
    'Content-Type': 'application/json-patch+json'
}

@deposit_controller.route('/api/add-deposit', methods=['POST'])
def add_deposit():
    data = request.json
    if not validate_amount(data['Amount']):
        return {'status': 'Negative amount not supported' }, 400
    else:
        r = requests.post('http://localhost:7071/api/Interest_Rate_Calculator', json={"Amount": data['Amount']}, headers=headers)
        response = r.json()
        with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
            try:
                conn.execute("PRAGMA foreign_keys = ON")
                cursor = conn.cursor()

                currentAmountQuery = "SELECT Amount FROM Account WHERE BankUserId = ?"
                updateAccountAmountQuery = "UPDATE Account SET ModifiedAt = datetime('now'), Amount = ? WHERE BankUserId = ?"
                insertDepositAmountQuery = "INSERT INTO Deposit(BankUserID, CreatedAt, Amount) VALUES (?, datetime('now'), ?)"

                currentAmmount = cursor.execute(currentAmountQuery, (data['BankUserId'],)).fetchone()[0]
                if not currentAmmount:
                    return {'status': 'Given user doesn\'t have an account yet'}, 404

                newAmmount = currentAmmount + response['amount_with_interest']
                cursor.execute(updateAccountAmountQuery, (newAmmount, data['BankUserId']))
                cursor.execute(insertDepositAmountQuery, (data['BankUserId'], response['amount_with_interest']))
                conn.commit()
            except sqlite3.Error as e:
                return {'Status': str(e)}, 400
        return {'Status':  'success'}, 201

@deposit_controller.route('/api/list-deposits/<BankUserId>', methods=['GET'])
def list_deposits(BankUserId):
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        listAllDepositsQuery = "SELECT * FROM Deposit WHERE BankUserId = ?"
        cursor = conn.cursor()
        try:
            deposits = cursor.execute(listAllDepositsQuery, (BankUserId,)).fetchall()
            return {'Data':  deposits}, 200
        except sqlite3.Error as e:
            return {'Status': str(e)}, 400


def validate_amount(amount: int)-> bool:
    if amount < 1:
        return False
    else:
        return True
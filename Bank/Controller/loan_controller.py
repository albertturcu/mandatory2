import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
import requests
load_dotenv()


loan_controller = Blueprint('loan_controller', __name__)
headers = {
    'Content-Type': 'application/json-patch+json'
}

@loan_controller.route('/api/create-loan', methods=['POST'])
def create_loan():
    data = request.json
    selectAccountAmountQuery = "SELECT Amount FROM Account WHERE BankUserId = ?"
    insertLoanDetailsQuery = "INSERT INTO Loan(BankUserId, CreatedAt, ModifiedAt, Amount) VALUES (?, datetime('now'), datetime('now'), ?)"
    updateAccountAmountQuery = "UPDATE Account SET Amount = ?, ModifiedAt = datetime('now') WHERE BankUserId = ?"
    currentAccountAmountQuery = "SELECT Amount FROM Account WHERE BankUserId = ?"

    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        cursor = conn.cursor()

        try:
            accountAmount = cursor.execute(selectAccountAmountQuery, (data['BankUserId'], )).fetchone()[0]
            if not validate_amount(data['LoanAmount']):
                return {'Status': 'Negative loan is not possible'}, 200

            r = requests.post('http://localhost:7071/api/Loan_Algorithm', json={"Loan": data['LoanAmount'], "Amount": accountAmount}, headers=headers)
            isValidLoan = r.status_code

            if isValidLoan == 200:
                currentAccountAmount = cursor.execute(currentAccountAmountQuery, (data['BankUserId'],)).fetchone()[0]
                newAccountAmount = currentAccountAmount + data['LoanAmount']
                cursor.execute(insertLoanDetailsQuery, (data['BankUserId'], data['LoanAmount']))
                cursor.execute(updateAccountAmountQuery, (newAccountAmount, data['BankUserId']))
                conn.commit()
                return {'Status': 'Loan Approved'}, 200
            elif isValidLoan == 403:
                return {'Status': 'Invalid Loan'}, 403
            else:
                return {'Status': 'Something went wrong'}, 404
        except sqlite3.Error as e:
            return {'Status': str(e)}, 500

@loan_controller.route('/api/pay-loan', methods=['POST'])
def pay_loan():
    data = request.json
    currentAccountAmountQuery = "SELECT Amount FROM Account WHERE BankUserId = ?"
    currentLoanAmountQuery = "SELECT Amount FROM Loan WHERE Id = ?"
    updateLoanAmountQuery = "UPDATE Loan SET Amount = 0, ModifiedAt = datetime('now') WHERE Id = ?"
    updateAccountAmountQuery = "UPDATE Account SET Amount = ?, ModifiedAt = datetime('now') WHERE BankUserId = ?"


    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        cursor = conn.cursor()
        currentAccountAmount = cursor.execute(currentAccountAmountQuery, (data['BankUserId'],)).fetchone()[0]
        currentLoanAmount = cursor.execute(currentLoanAmountQuery, (data['LoanId'],)).fetchone()[0]
        if currentLoanAmount == 0:
            return {'Status': 'Loan is paid for the given loan id'}, 404

        if currentAccountAmount - currentLoanAmount >= 0:
            newAccountAmount = currentAccountAmount - currentLoanAmount
            print(newAccountAmount)
            cursor.execute(updateLoanAmountQuery, (data['LoanId'],))
            cursor.execute(updateAccountAmountQuery, (newAccountAmount, data['BankUserId']))
            conn.commit()
            return {'Status': 'Loan was successfully paid'}, 200
        else:
            return {'Status': 'Unable to pay loan: Not enough money in the account'}, 404

@loan_controller.route('/api/list-loans/<BankUserId>', methods=['GET'])
def list_loans(BankUserId):
    selectNotPaidLoansQuery = "SELECT * FROM Loan WHERE BankUserId = ? and Amount > 0"
    with sqlite3.connect("Bank.sqlite", check_same_thread=False) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(selectNotPaidLoansQuery, (BankUserId,))
            allLoans = cursor.fetchall()
            if len(allLoans) > 0:
                return {'Data': allLoans}, 200
            else:
                return {'Status': 'There are no current loans for the given user'}, 200
        except sqlite3.Error as e:
            return {'Status': str(e)}, 500

def validate_amount(amount: int)-> bool:
    if amount < 1:
        return False
    else:
        return True

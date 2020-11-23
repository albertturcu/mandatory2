import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()

year_controller = Blueprint('year_controller', __name__)
@year_controller.route('/api/create-year', methods=['POST'])
def create_year():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO SkatYear(Label, CreatedAt, ModifiedAt, StartDate, EndDate) VALUES(?,datetime('now'),datetime('now'),?,?)"
        query_get_skatusers = "SELECT * FROM SkatUser"
        year = request.json
        try:
            cursor.execute( query, (year['Label'], year['StartDate'], year['EndDate'] ))
            cursor.execute(query_get_skatusers)
            skatYearId = cursor.lastrowid
            skat_users = cursor.fetchall()
            amount = 0
            for user in skat_users:
                query_skat_year = "INSERT INTO SkatUserYear(SkatUserId, SkatYearId, UserId, IsPaid, Amount) VALUES(?,?,?,?,?)"
                cursor.execute(query_skat_year, (user[0], skatYearId, user[1], 0, amount ))
                conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

@year_controller.route('/api/get-skat-year/<Id>', methods=['GET'])
def get_skat_year(Id):
        with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
            query = "SELECT * FROM SkatYear WHERE Id = ?"
            cursor = conn.cursor()
            try:
                cursor.execute(query, (Id, ))
                data = cursor.fetchone()
                if data:
                    return {'Skat Year': data}, 200
                else:
                    return {'Skat Year': 'year not found'}, 200
            except sqlite3.Error as e:
                return {'status': str(e)}, 500

@year_controller.route('/api/get-skat-years', methods=['GET'])
def get_skat_years():
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "SELECT * FROM SkatYear"
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return {'status': 'success', 'data': data }, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500

@year_controller.route('/api/update-year/<Id>', methods=['PATCH'])
def update_year(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "UPDATE SkatYear SET Label = ?, ModifiedAt = datetime('now'), StartDate = ? , EndDate = ? WHERE Id = ? "
        cursor = conn.cursor()
        year = request.json
        try:
            cursor.execute(query, (year["Label"], year["StartDate"],year["EndDate"], Id ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
        
@year_controller.route('/api/delete-year/<Id>', methods=['DELETE'])
def delete_year(Id):
    with sqlite3.connect(environ.get('DATABASE_URL'), check_same_thread=False) as conn:
        query = "DELETE FROM SkatYear WHERE Id=?"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (Id, ))
            conn.commit()
            return {'status': 'success'}, 200
        except sqlite3.Error as e:
            return {'status': str(e)}, 500
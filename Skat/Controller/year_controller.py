import sqlite3
from flask import Blueprint, request
from os import environ
from dotenv import load_dotenv
load_dotenv()

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/create-year', methods=['POST'])
def create_year():
    pass
    
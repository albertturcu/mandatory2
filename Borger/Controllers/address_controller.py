from flask import Blueprint


address_controller = Blueprint('address_controller', __name__)

@address_controller.route('/api/createAddress', methods=['POST'])
def create_address():
    return 'it works!'

@address_controller.route('/api/getAddress', methods=['GET'])
def get_address():
    return 'it works!'

@address_controller.route('/api/getAllAddresss', methods=['GET'])
def get_all_addresss():
    return 'it works!'

@address_controller.route('/api/updateAddress', methods=['PATCH'])
def update_address():
    return 'it works!'

@address_controller.route('/api/deleteAddress', methods=['DELETE'])
def delete_address():
    return 'it works!'
from flask import Flask, g
from Controllers.user_controller import user_controller
from Controllers.address_controller import address_controller


app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(address_controller)

if __name__ == '__main__':
    app.run(host='localhost', load_dotenv=True, port=5004, use_reloader=True)
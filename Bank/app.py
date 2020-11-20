from flask import Flask
from Controller.user_controller import user_controller
from Controller.account_controller import account_controller
from Controller.deposit_controller import deposit_controller
from Controller.loan_controller import loan_controller

app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(account_controller)
app.register_blueprint(deposit_controller)
app.register_blueprint(loan_controller)

if __name__ == '__main__':
    app.run(host='localhost', load_dotenv=True, port=5005, use_reloader=True)
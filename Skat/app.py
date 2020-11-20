from flask import Flask
from Controller.user_controller import user_controller
# from Controller.year_controller import year_controller

app = Flask(__name__)
app.register_blueprint(user_controller)
# app.register_blueprint(year_controller)


if __name__ == '__main__':
    app.run(host='localhost', load_dotenv=True, port=5006, use_reloader=True)
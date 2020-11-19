from flask import Flask


app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='localhost', load_dotenv=True, port=5006, use_reloader=True)
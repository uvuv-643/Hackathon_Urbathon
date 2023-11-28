from flask import Flask

from urbaton import rest_init, flask_config

app = Flask(__name__)

app = rest_init(app)
app = flask_config(app)
if __name__ == '__main__':
    app.run(debug=True)

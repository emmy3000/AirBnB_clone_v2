#!/usr/bin/python3
"""
Flask web application with two routes.
The web application listens on 0.0.0.0, port 5000.

Routes:
    /: display "Hello HBNB!"
    /hbnb: display "HBNB"
    /c/<text>: display "C " followed by the value of the 'test'
    variable
    Mandatory use of `strict_slashes=False` in route definition.
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when accessing the root URL.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB" when accessing the '/hbnb' URL.
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """
    Displays "C " followed by the value of the 'text' variable
    with underscores replaced by spaces.
    """
    return 'C {}'.format(escape(text.replace('_', ' ')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
"""
Flask web application with multiple routes.
The web application listens on 0.0.0.0, port 5000.

Routes:
    /: display "Hello HBNB!"
    /hbnb: display "HBNB"
    /c/<text>: display "C " followed by the value of the 'text' variable
    /python/(<text>): display "Python " followed by the value of the variable
                        (replace underscore '_' symbol with a space)
    The default value of 'text' is "is cool"
    /number/<n>: display "<n> is a number" only if 'n' is an integer
    /number_template/<n>: Displays a custom HTML page if the value is an
    integer 89.
    /number_odd_or_even/<n>: Displays a custom HTML page indicating whether
    the number is even or odd.

Mandatory use of `strict_slashes=False` in route definition.
"""
from flask import Flask, render_template
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
    Displays "C " followed by the value of the 'text' variable,
    with underscores replaced by spaces.
    """
    return 'C {}'.format(escape(text.replace('_', ' ')))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """
    Displays "Python " followed by the value of the 'text' variable,
    with underscores replaced by spaces. Uses 'is cool' as the default value.
    """
    return 'Python {}'.format(escape(text.replace('_', ' ')))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Displays "<n> is a number" only if 'n' is an integer.
    Otherwise, it returns a 404 Not Found error.
    """
    if isinstance(n, int):
        return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Displays a custom HTML page if the value is an integer 89.
    """
    return render_template('6-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Displays a custom HTML page indicating whether the number
    is even or odd.
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

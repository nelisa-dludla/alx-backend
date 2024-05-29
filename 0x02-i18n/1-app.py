#!/usr/bin/env python3
'''
A simple Flask app with Babel
'''

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    '''
    Defines the Config class
    '''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def hello_world():
    '''
    Renders 1-index.html
    '''
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

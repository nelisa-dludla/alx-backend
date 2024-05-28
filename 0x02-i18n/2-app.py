#!/usr/bin/env python3
'''
A simple Flask app with Babel
'''

from flask import Flask, render_template, request
from flask_babel import Babel

class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale():
    supported_languages = request.accept_languages.languages()

    for language in supported_languages:
        if language in app.config['LANGUAGES']:
            return language

@app.route('/')
def hello_world():
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/env python3
'''
A simple Flask app with Babel
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _


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


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    '''
    Determines the ideal language amongst the
    supported languages
    '''
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    supported_languages = request.accept_languages.languages()

    for language in supported_languages:
        if language in app.config['LANGUAGES']:
            return language

    return app.config['BABEL_DEFAULT_LOCALE']


def get_user():
    '''
    Searches url for a user
    '''
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    else:
        return None


@app.before_request
def before_request():
    '''
    Calls get_user
    '''
    g.user = get_user()


@app.route('/')
def hello_world():
    '''
    Renders 3-index.html
    '''
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

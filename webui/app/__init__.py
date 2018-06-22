"""
module contains functions for creating and configuring a flask app
"""
import os

from flask import Flask

from .config import config
default_config_name = os.getenv('FLASK_CONFIG', 'default')
app_config = config[default_config_name]


def add_views(_app):
    """
    add views to application
    Args:
        _app: flask application
    """
    from .views import IndexView

    _app.add_url_rule('/', view_func=IndexView.as_view('index'))


def create_app(config_name=default_config_name):
    """create, configure and return a flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    add_views(app)
    return app

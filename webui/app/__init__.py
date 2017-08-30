"""
module contains functions for creating and configuring a flask app
"""
from flask import Flask

from app import config


def configure_app(app):
    """
    configure application with config file
    Args:
        app: flask application
    """
    app.config.from_object(config)


def add_views(_app):
    """
    add views to application
    Args:
        _app: flask application
    """
    from app.views import IndexView

    _app.add_url_rule('/', view_func=IndexView.as_view('index'))


def create_app():
    """create, configure and return a flask app"""
    app = Flask(__name__)
    configure_app(app)
    add_views(app)
    return app

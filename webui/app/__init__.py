from flask import Flask

from app import config


def configure_app(app):
    """
    Configure Flask application from config file
    """
    app.config.from_object(config)


def add_views(_app):
    """
    Register views in app
    """
    from app.views import IndexView

    _app.add_url_rule('/', view_func=IndexView.as_view('index'))


def create_app():
    """
    Creates Flask application
    """
    _app = Flask(__name__)
    configure_app(_app)
    add_views(_app)
    return _app

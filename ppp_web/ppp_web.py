"""Run"""
import os

from flask import Flask, send_from_directory
from flask import request
from flask import send_file

try:
    from ppp_web.config import config
except ModuleNotFoundError:
    from config import config


env_name = os.getenv('ENV', 'default')
app_config = config[env_name]


def add_views(_app):
    """
    add views to application
    Args:
        _app: flask application
    """
    try:
        from ppp_web.views import IndexView
    except ModuleNotFoundError:
        from views import IndexView
    _app.add_url_rule('/', view_func=IndexView.as_view('index'))

    @_app.route('/favicon.ico')
    def favicon():
        """Renders favicon."""
        return send_from_directory(
            os.path.join(_app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon')

    @_app.route('/export', method='POST')
    def export():
        # need to catch post form fields and send file which was already stored
        pdf_doc_file_path = request.data['pdf_doc_file_path'];
        mime_type = request.data['mime_type'];
        attachment_filename = request.data['attachment_filename'];
        return send_file(pdf_doc_file_path,
                         as_attachment=True,
                         mimetype=mime_type,
                         attachment_filename=attachment_filename)


def create_app(config_name=env_name):
    """create, configure and return a flask app"""
    new_app = Flask(__name__)
    new_app.config.from_object(config[config_name])
    add_views(new_app)
    return new_app


app = create_app()


def run():
    """run"""
    if env_name in ('development', 'default'):
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run()


if __name__ == '__main__':
    run()

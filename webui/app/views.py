from flask import render_template
from flask import redirect
from flask import url_for
from flask.views import MethodView

from werkzeug.utils import secure_filename


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        return 'Hello, world (POST)!'

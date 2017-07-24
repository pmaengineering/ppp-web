from flask import render_template
from flask.views import MethodView


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        return 'Hello, world (POST)!'

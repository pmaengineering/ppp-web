import shlex
import subprocess
import tempfile

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from flask.views import MethodView

from app import config


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        file = request.files['file']
        if file and '.xls' not in file.filename:
            flash("Uploaded file is not an .xls or .xlsx file", "error")
            return redirect(url_for('index'))

        extension = file.filename.split('.')[-1]
        file_path = tempfile.mktemp(suffix='.' + extension)
        file.save(file_path)

        language = request.form.get('language', 'English')
        out_format = request.form.get('format', 'html')

        output_file_name = file.filename + '.' + out_format
        output_file_path = tempfile.mktemp(suffix=output_file_name)

        preset = request.form.get('preset', 'developer')

        options = request.form.getlist('options')

        if preset != 'custom':
            options = ['preset=' + preset]

        command_line = " ".join((
            config.python_executable,
            '-m pmix.ppp',
            file_path,
            "-l " + language,
            "-f " + out_format,
            "-o " + output_file_path,
            *(' --{}'.format(option) for option in options)
        ))

        args = shlex.split(command_line)
        p = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        stdout = p.stdout.read().decode()
        stterr = p.stderr.read().decode()

        return send_file(output_file_path,
                         as_attachment=True,
                         mimetype='text/html',
                         attachment_filename=output_file_name)

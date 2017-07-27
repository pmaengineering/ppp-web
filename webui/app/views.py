import os
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
        # check if used uploaded an excel file
        file = request.files['file']
        if file and '.xls' not in file.filename:
            flash("Uploaded file is not an .xls or .xlsx file", "error")
            return redirect(url_for('index'))

        # build dict for HTML conversions for future code simplicity
        converters = {
            'pdf': self._convert_to_pdf,
            'doc': self._convert_to_doc
        }

        # save file to /tmp folder
        extension = os.path.splitext(file.filename)[1]
        uploaded_file_path = tempfile.mktemp(suffix=extension)
        file.save(uploaded_file_path)

        # get output format
        output_format = request.form.get('format')

        # process output format and mime type for downloading
        post_process_to = None
        mime_type = 'application/text'
        if output_format == 'html':
            mime_type = 'text/html'

        if output_format in ('pdf', 'doc'):
            post_process_to = output_format
            output_format = 'html'

        # convert uploaded file to html
        output_file_name = file.filename + '.' + output_format
        output_file_path = tempfile.mktemp(suffix=output_file_name)
        command_line = self._build_pmix_ppp_tool_run_cmd(uploaded_file_path,
                                                         output_format,
                                                         output_file_path)
        _, stderr = self._run_background_process(command_line)

        # if pmix.ppp tool wrote something to stderr, we should show it to user
        if stderr:
            flash("STDERR:\n{}".format(stderr), "error")
            return redirect(url_for('index'))

        # output_file_path now exists and refers to converted html file
        # located at /tmp folder
        file_path = output_file_path
        file_name = output_file_name

        # if output format is PDF or DOC
        if post_process_to:
            converter = converters[post_process_to]
            file_name, file_path, mime_type = converter(output_file_path)

        return send_file(file_path,
                         as_attachment=True,
                         mimetype=mime_type,
                         attachment_filename=file_name)

    def _convert_to_pdf(self, file_path):
        pdf_file_path = file_path.replace('.html', '.pdf')
        command_line = " ".join((
            config.wkhtmltopdf_executable,
            file_path,
            pdf_file_path
        ))
        self._run_background_process(command_line)
        _, pdf_file_name = os.path.split(pdf_file_path)
        mime_type = 'text/pdf'
        return pdf_file_name, pdf_file_path, mime_type

    def _convert_to_doc(self, file_path):
        doc_file_path = file_path.replace('.html', '.docx')
        os.rename(file_path, doc_file_path)
        _, doc_file_name = os.path.split(doc_file_path)
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        return doc_file_name, doc_file_path, mime_type

    def _run_background_process(self, command_line):
        args = shlex.split(command_line)
        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.wait()
        stdout = process.stdout.read().decode().strip()
        stderr = process.stderr.read().decode().strip()

        return stdout, stderr

    def _build_pmix_ppp_tool_run_cmd(self, in_file_path, out_format,
                                     out_file_path):

        language = request.form.get('language')
        preset = request.form.get('preset', 'developer')
        options = request.form.getlist('options')
        if preset != 'custom':
            options = ['preset ' + preset]

        command_line = " ".join((
            config.python_executable,
            '-m pmix.ppp',
            in_file_path,
            "-l " + language,
            "-f " + out_format,
            *('--{}'.format(option) for option in options),
            "-o " + out_file_path
        ))

        return command_line

"""module contains main view class"""
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
    """
    Index view class with two handlers for GET and POST requests
    """
    def get(self):
        """GET request handler. Just renders HTML for main page"""
        return render_template('index.html')

    def post(self):
        """POST request handler. Processes form data"""

        # check if user uploaded an excel file
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

        # return file as response attachment, so browser will start download
        return send_file(file_path,
                         as_attachment=True,
                         mimetype=mime_type,
                         attachment_filename=file_name)

    def _convert_to_pdf(self, file_path):
        """
        converts html file to pdf file on the disk
        :param file_path: path to html file
        """
        # create output file path
        pdf_file_path = file_path.replace('.html', '.pdf')

        # create command line string for html->pdf converter
        command_line = " ".join((
            config.wkhtmltopdf_executable,
            file_path,
            pdf_file_path
        ))

        # run converter
        self._run_background_process(command_line)

        # get file name
        _, pdf_file_name = os.path.split(pdf_file_path)
        mime_type = 'text/pdf'

        # return file name, path and mime type to be used in response
        return pdf_file_name, pdf_file_path, mime_type

    def _convert_to_doc(self, file_path):
        """
        "converts" html file to doc file
        :param file_path: html file path on disk
        :return: 
        """

        # get doc file path
        doc_file_path = file_path.replace('.html', '.docx')
        # rename file
        os.rename(file_path, doc_file_path)
        # get file name
        _, doc_file_name = os.path.split(doc_file_path)
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        # return file name, path and mime type to be used in response
        return doc_file_name, doc_file_path, mime_type

    def _run_background_process(self, command_line):
        """
        executes external command
        :param command_line: command line string
        :return: stdout and stdin of executed command
        """

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
        """
        builds command line string for ppp tool 
        :param in_file_path: input excel file path
        :param out_format: output format
        :param out_file_path: output file path
        :return: command line string
        """
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

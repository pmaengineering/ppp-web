"""Views for application."""
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

from app import config  # TODO: Refactor to remove IDE error/run consistently.


class IndexView(MethodView):
    """
    This method responsible only for returning rendered template
    """
    @staticmethod
    def get():
        """Get method."""
        return render_template('index.html')

    def post(self):
        """
        This method processes uploaded file .xlsx file and returns
        converted file
        """

        # check if user uploaded an excel file
        file = request.files['file']
        if file and '.xls' not in file.filename:  # TODO: Refactor, endswith.
            flash("Uploaded file is not an .xls or .xlsx file", "error")
            return redirect(url_for('index'))

        # build dict for HTML conversions for future code simplicity
        converters = {
            'pdf': self._convert_to_pdf,
            'doc': self._convert_to_doc
        }

        # save file to /tmp folder
        extension = os.path.splitext(file.filename)[1]
        _, uploaded_file_path = tempfile.mkstemp(suffix=extension)
        file.save(uploaded_file_path)

        # get output format
        output_format = request.form.get('format')

        # process output format and mime type for downloading
        post_process_to = None
        mime_type = 'text/html' if output_format == 'html'\
            else 'application/text'

        if output_format in ('pdf', 'doc'):
            post_process_to = output_format
            output_format = 'html'

        # convert uploaded file to html
        out_extension = '.' + output_format
        output_file_name = file.filename.replace(extension, out_extension)
        _, output_file_path = tempfile.mkstemp(suffix=out_extension)
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
            file_path, mime_type = converter(output_file_path)
            file_name = file_name.replace('.html', '.' + post_process_to)

        # return converted file to user
        return send_file(file_path,
                         as_attachment=True,
                         mimetype=mime_type,
                         attachment_filename=file_name)

    def _convert_to_pdf(self, file_path):
        """This method converts .html file to .pdf file

        Uses external tool named `wkhtmltopdf`.

        Returns:
             Path to converted file and mime type.
        """
        pdf_file_path = file_path.replace('.html', '.pdf')
        command_line = " ".join((
            config.wkhtmltopdf_executable,
            file_path,
            pdf_file_path
        ))
        self._run_background_process(command_line)
        _, pdf_file_name = os.path.split(pdf_file_path)
        mime_type = 'text/pdf'
        return pdf_file_path, mime_type

    @staticmethod
    def _convert_to_doc(file_path):
        """This method renames .html file to .doc file.

        Returns:
            path to renamed file and mime type for word files.
        """
        doc_file_path = file_path.replace('.html', '.doc')
        os.rename(file_path, doc_file_path)
        _, doc_file_name = os.path.split(doc_file_path)
        mime_type = 'application/vnd.openxmlformats-officedocument.' \
                    'wordprocessingml.document'
        return doc_file_path, mime_type

    @staticmethod
    def _run_background_process(command_line):
        """This method runs external program using command line interface.

        Returns:
             stdout,stdin: Of executed program.
        """
        args = shlex.split(command_line)
        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.wait()
        stdout = process.stdout.read().decode().strip()
        stderr = process.stderr.read().decode().strip()

        return stdout, stderr

    @staticmethod
    def _build_pmix_ppp_tool_run_cmd(in_file_path, out_format,
                                     out_file_path):
        """This method build command line command to run pmix.ppp tool.

        Returns:
            string: Command.
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

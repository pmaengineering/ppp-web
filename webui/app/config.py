"""module contains flask application settings"""
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bin_dir = os.path.join(base_dir, 'bin')

wkhtmltopdf_executable = os.path.join(bin_dir, 'wkhtmltopdf')
python_executable = {
    'linode': '/home/pydevd/projects/conv-webui/.venv/bin/python3'
}['linode']

THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "?x1234567890x!"
SECRET_KEY = "!x1234567890x?"

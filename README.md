# ppp-web
Web server and client application for Pretty PDF Printer, a package to convert ODK XlsForms to human readable formats.

# Application brief description

Application contains only one page with web form, where user can upload an ODK XlsForms file
for conversion to HTML, PDF of DOC format.

#### UI libraries:
- [Twitter Bootstrap](http://getbootstrap.com/)
- [Bootstrap File Input](http://plugins.krajee.com/file-input)
- [jQuery v2.2.4](https://jquery.com/)
- [Notify.js](https://notifyjs.com/)

#### Backend libraries:
- [Flask](http://flask.pocoo.org/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)


#### Tips
- Backend: conversion to DOC format implemented as conversion to HTML file and returning this HTML file to user
with .doc extension instead of .html, as office programs understands how to render such files.
- Backend: conversion to PDF format implemented as conversion to HTML with next conversion to PDF using **wkhtmltopdf** external tool.
- UI: After successful uploading, form will be cleared automatically.
- UI: If something was wrong while processing the file, page will be reloaded and error message will be shown.
- UI: manually selecting/deselecting conversion options will activate "Custom" preset button.


# Deployment (Ubuntu)

Update system and install required packages

``$ apt-get update``

``$ apt-get install htop libfontconfig1 libxrender1 python3-pip python3-dev python3-venv nginx git vim``

Clone project from repo

``$ cd /opt``

``$ git clone https://github.com/PMA-2020/ppp-web.git``

Create virtual environment

``/opt $ python3 -m venv .venv``

``/opt $ source .venv/bin/activate``

``/opt $ pip install --upgrade pip``

Install project dependencies

``/opt $ pip install -r requirements.txt``

Install pmix package

``/opt $ pip install -r https://raw.githubusercontent.com/joeflack4/pmix/ppp/requirements.txt``

``/opt $ pip install pip install https://github.com/joeflack4/pmix/archive/ppp.zip``

Change python executable path in ``webui/app/config.py``

``/opt $ cp webui``

``/opt/webui $ vim app/config.py``

Set variable ``python_executable`` to

``python_executable='/opt/ppp-web/.venv/bin/python3'``

Set execution flag for ``bin/wkhtmltopdf``

``/opt/webui $ chmod +x bin/wkhtmltopdf``

Run the app in background:

``/opt/webui $ gunicorn -b 0.0.0.0:8080 uwsgi:app &``

Open web interface at address:

``https://<server-ip>:8080``
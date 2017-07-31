# ppp-web
Web server and client application for Pretty PDF Printer, a package to convert ODK XlsForms to human readable formats.

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

https://<server-ip>:8080
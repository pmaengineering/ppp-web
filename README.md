# PPP-Web
Web server and client application for Pretty PDF Printer, a package to convert ODK XlsForms to human readable formats.

# Deployment (Ubuntu)

Update system and install required packages

`$ apt-get update`

`$ apt-get install htop libfontconfig1 libxrender1 python3-pip python3-dev python3-venv nginx git vim`

Clone project from repo

`$ cd /opt`

`/opt $ git clone https://github.com/PMA-2020/ppp-web.git`

Create virtual environment

`/opt $ cd ppp-web`

`/opt/ppp-web $ python3 -m venv .venv`

`/opt/ppp-web $ source .venv/bin/activate`

`/opt/ppp-web $ pip install --upgrade pip`

Install project dependencies

`/opt/ppp-web $ pip install -r requirements.txt`

Install pmix package

`/opt/ppp-web $ pip install -r https://raw.githubusercontent.com/<git-suburl>/requirements.txt`  
Example of <git-suburl>: `jkpr/pmix/develop`

`/opt/ppp-web $ pip install https://github.com/<git-suburl>`  
Example of <git-suburl>: `joeflack4/pmix/archive/ppp.zip`

Change Python executable path

`/opt/ppp-web $ cd webui`

`/opt/ppp-web/webui $ vim app/config.py`

Set Python executable variable

`python_executable='/opt/ppp-web/.venv/bin/python3'`

Set execution flag for dependency *wkhtmltopdf*

`/opt/ppp-web/webui $ chmod +x bin/wkhtmltopdf`

Run the app in background

`/opt/ppp-web/webui $ gunicorn -b 0.0.0.0:8080 uwsgi:app &`

Open web interface at address

`https://<server-ip>:8080`

# Upgrading Dependencies
#### Log in to server
`ssh <server>` and enter password when prompted. 

Example: `root@192.155.80.11`
#### Activate virtual environment
`cd /opt/ppp-web`
`source .venv/bin/activate`
#### Upgrade dependency
`python -m pip install <url-to-dependency> --upgrade`

Example: `python -m pip install git+https://github.com/jkpr/pmix@develop --upgrade` 

#### Restart server (if necessary)  
###### Find process ID  
The server that PPP-Web uses is called "gunicorn", so: `ps -e | grep gunicorn`  

###### Kill process  
`kill -9 <ID>`, where "<ID>" is the one found in previous step.
###### Start new process
`cd webui`

`gunicorn -b 0.0.0.0:8080 uwsgi:app &`

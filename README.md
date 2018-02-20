# PPP-Web
Web server and client application for Pretty PDF Printer, a package to convert ODK XlsForms to human readable formats.


# Application Internals

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


# Deployment

#### Update system and install required packages
This deployment guide is written for [*Ubuntu*](https://www.linode.com/docs/getting-started/#ubuntu-debian). For other Linux distributions, please refer to this [handy setup guide](https://www.linode.com/docs/getting-started/#install-software-updates), especially if using *Linode*.

`apt-get update && apt-get upgrade`

> **Note**  
> Ubuntu may prompt you when the Grub package is updated. If prompted, select keep the local version currently installed.

`apt-get install htop libfontconfig1 libxrender1 python3-pip python3-dev python3-venv nginx git vim`

#### Clone project from repo

`cd /opt`

`/opt $` `git clone https://github.com/PMA-2020/ppp-web.git`

#### Create virtual environment

`/opt $` `cd ppp-web`

`/opt/ppp-web $` `python3 -m venv .venv`

`/opt/ppp-web $` `source .venv/bin/activate`

`/opt/ppp-web $` `pip install --upgrade pip`

#### Dependencies
Install project dependencies

`/opt/ppp-web $` `pip install -r requirements.txt`

Install pmix package

`/opt/ppp-web $ pip install -r https://raw.githubusercontent.com/<git-suburl>/requirements.txt`  
> **Example**  
> `pip install -r https://raw.githubusercontent.com/jkpr/pmix/develop/requirements.txt`

> **Note**  
> You may experience a `DistutilsError` related to the `cairocffi` package. If this occurs, it is likely OK to ignore, as this is a peer dependency and not required for PPP-Web.

`/opt/ppp-web $ pip install https://github.com/<git-suburl>`  
> **Examples**
> `pip install https://github.com/jkpr/pmix/archive/develop.zip`
> `pip install https://github.com/joeflack4/pmix/archive/ppp.zip`

#### Additional Configuration
Change Python executable path

`/opt/ppp-web $` `cd webui`

`/opt/ppp-web/webui $` `vim app/config.py`

Set Python executable variable

`python_executable='/opt/ppp-web/.venv/bin/python3'`

Set execution flag for dependency *wkhtmltopdf*

`/opt/ppp-web/webui $` `chmod +x bin/wkhtmltopdf`

#### Run server process
Run the app in background

`/opt/ppp-web/webui $` `gunicorn -b 0.0.0.0:8080 uwsgi:app &`

Open web interface at address

`https://<server-ip>:8080`


# Maintenance
## Upgrading Dependencies
#### Log in to server
`ssh <server>` and enter password when prompted. 

Example: `root@192.155.80.11`

#### Activate environment
> Common Workflows > [Activate virtual environment](#activate-virtual-environment)

#### Upgrade dependency
`python -m pip install <url-to-dependency> --upgrade`

Example: `python -m pip install git+https://github.com/jkpr/pmix@develop --upgrade` 

#### Restart server
> Common Workflows > [Restart server](#restarting-the-server)


# Common Workflows
## Starting the server
#### Activate environment
> Common Workflows > [Activate virtual environment](#activate-virtual-environment)

#### Run server process
`cd /opt/ppp-web/webui`

`/opt/ppp-web/webui $` `gunicorn -b 0.0.0.0:8080 uwsgi:app &`

## Restarting the server 
#### Find process ID  
The server that PPP-Web uses is called "gunicorn", so: `ps -e | grep gunicorn`  

#### Kill process  
`kill -9 <ID>`, where "<ID>" is the one found in previous step.
#### Start new process
> Common Workflows > [Starting the server](#starting-the-server)

## Activate virtual environment
`cd /opt/ppp-web`
`/opt/ppp-web $` `source .venv/bin/activate`

# PPP-Web
Web server and client application for Pretty PDF Printer, a package to convert ODK XlsForms to human readable formats.


# Application Internals

Application contains only one page with web form, where user can upload an ODK XlsForms file
for conversion to HTML, PDF of DOC format.

#### UI libraries:
- [Twitter Bootstrap](http://getbootstrap.com/)
- [Bootstrap File Input](http://plugins.krajee.com/file-input)
- [jQuery v3.2.1](https://jquery.com/)
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

#### 1. Update system and install required packages
This deployment guide is written for [*Ubuntu*](https://www.linode.com/docs/getting-started/#ubuntu-debian). For other Linux distributions, please refer to this [handy setup guide](https://www.linode.com/docs/getting-started/#install-software-updates), especially if using *Linode*.

`apt-get update && apt-get upgrade`

> **Note**  
> Ubuntu may prompt you when the Grub package is updated. If prompted, select keep the local version currently installed.

`apt-get install libfontconfig1 libxrender1 python3-pip python3-dev python3-venv git`

#### 2. Clone project from repo

`cd /opt`

`/opt $` `git clone https://github.com/PMA-2020/ppp-web.git`

#### 3. Create virtual environment

`/opt $` `cd ppp-web`

`/opt/ppp-web $` `python3 -m venv .venv`

`/opt/ppp-web $` `source .venv/bin/activate`

`/opt/ppp-web $` `pip3 install --upgrade pip3`

#### 4. Dependencies
`/opt/ppp-web $` `pip3 install -r requirements.txt`

> **Note**  
> You may experience a `DistutilsError` related to the `cairocffi` package. If this occurs, it is likely OK to ignore, as this is a peer dependency and not required for PPP-Web.

`/opt/ppp-web $ pip3 install https://github.com/<git-suburl>`  
> **Examples**  
> `pip3 install https://github.com/PMA-2020/ppp/archive/develop.zip`  
> `pip3 install https://github.com/joeflack4/pmix/archive/ppp.zip`

#### 5. Required Configuration
##### Change Python executable path
Edit config.py  
`/opt/ppp-web $` `cd webui`  
`/opt/ppp-web/webui $` `nano app/config.py`

Set Python executable variable  
`PYTHON_PATH='/opt/ppp-web/.venv/bin/python3'`


##### Set execution flag for dependency *wkhtmltopdf*

`/opt/ppp-web/webui $` `chmod +x bin/wkhtmltopdf`

#### 6. Set up logging
`mkdir logs/`  
`touch access-logfile.log && touch error-logfile.log`

#### 7. Run server process
Run the app in background

`/opt/ppp-web/webui $` `gunicorn -b 0.0.0.0:8080 run:app &`

Open web interface at address

`https://<server-ip>:8080`

You're finished!


# Maintenance
## Upgrading PPP-Web
#### Log in to server & activate environment
> Common Workflows > [Logging in to server](#logging-in-to-server)  
> Common Workflows > [Activate virtual environment](#activate-virtual-environment)

There are several options from here. One option to get changes is to checkout a 
remote branch locally and reapply a change *config.py* as shown in the first 
part of step (5) in the *Deployment* section. Another option is to back up and 
clone a fresh copy of the repo. Another option is to stash any current changes, 
rebase/merge, and recover the stash. Another option is to commit any current 
changes and then do a rebase of the/a remote branch onto the/a local one. 
That's the one we'll show here.

#### Backup current install (optional)
This step is optional, as git in itself is a backup mechanism.

`cd /opt/`  
`mkdir _archive` *(if it doesn't exist)*  
`mv ppp-web _archive/DATE`  
> **Example**
> `mv ppp-web _archive/2018-02-20` 

#### Commit local changes
Add local changes to staging  
`git add .`

Commit local changes. If all you've done during/since deployment is change 
config.py, the following message should do.  
`git commit -m "Updated PYTHON_PATH path in config.py during deployment
installation process."`

#### Get remote changes
Add any additonal remotes if required to fetch from

`git remote add trunk https://github.com/PMA-2020/ppp-web.git`  
> **Example**  
> ```
> git remote add trunk https://github.com/PMA-2020/ppp-web.git && \
> git remote add joeflack4 https://github.com/joeflack4/ppp-web.git
> ```

Fetch changes

`git fetch --all`

Merge in changes using rebase
`git rebase REMOTE/BRANCH`
> **Example**  
> `git rebase trunk/master`

#### [Start](#starting-the-server) or [restart](#restarting-the-server) server
> Common Workflows > [Starting the server](#starting-the-server)

## Upgrading Dependencies
#### Log in to server & activate environment
> Common Workflows > [Logging in to server](#logging-in-to-server)  
> Common Workflows > [Activate virtual environment](#activate-virtual-environment)

#### Restart server
> Common Workflows > [Restart server](#restarting-the-server)

# Common Workflows
## Logging in to server
`ssh <server>` and enter password when prompted. 

> **Examples**  
> Production: `root@192.155.80.11`  
> Staging: `root@172.104.31.28`

## Starting the server
#### Activate environment
> Common Workflows > [Activate virtual environment](#activate-virtual-environment)

#### Run server process
`cd /opt/ppp-web/webui`  
`/opt/ppp-web/webui $` `gunicorn -b 0.0.0.0:8080 run:app &`

## Restarting the server 
#### Find process ID  
The server that PPP-Web uses is called "gunicorn", so...  
`ps -e | grep gunicorn`  

#### Kill process  
`kill -9 <ID>`, where `<ID>` is the one found in previous step.
#### Start new process
> Common Workflows > [Starting the server](#starting-the-server)

## Activate virtual environment
`cd /opt/ppp-web`  
`/opt/ppp-web $` `source .venv/bin/activate`

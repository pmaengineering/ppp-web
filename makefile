PYTHON=./env/bin/python3
SRC=./webui/
TEST=./test/

PYLINT=${PYTHON} -m pylint --output-format=colorized --reports=n
PYCODESTYLE=${PYTHON} -m pycodestyle
PYDOCSTYLE=${PYTHON} -m pydocstyle

LINT_SRC=${PYLINT} ${SRC}
LINT_TEST=${PYLINT} ${TEST}

CODE_SRC=${PYCODESTYLE} ${SRC}
CODE_TEST=${PYCODESTYLE} ${TEST}

DOC_SRC=${PYDOCSTYLE} ${SRC}
DOC_TEST=${PYDOCSTYLE} ${TEST}

MANAGE=${PYTHON} manage.py


.PHONY: lint linttest lintall pylint pylinttest pylintall code codetest codeall doc doctest docall test testdoc serve serve-local serve-heroku-local serve-staging-linode serve-production-linode serve-production-heroku serve-production serve-staging-heroku serve-staging shell db production staging production-linode staging-linode tags ltags upgrade-pmix-trunk-master upgrade-pmix-trunk-develop upgrade-pmix-joeflack4-master upgrade-pmix-joeflack4-develop upgrade-pmix upgrade-ppp-web-joeflack4-develop upgrade-ppp-web activate


# ALL LINTING
lint:
	${LINT_SRC} && ${CODE_SRC} && ${DOC_SRC}

linttest:
	${LINT_TEST} && ${CODE_TEST} && ${DOC_TEST}

lintall: lint linttest


# PYLINT
pylint:
	${LINT_SRC}

pylinttest:
	${LINT_TEST}

pylintall: pylint pylinttest

# PYCODESTYLE
code:
	${CODE_SRC}

codetest:
	${CODE_TEST}

codeall: code codetest


# PYDOCSTYLE
doc:
	${DOC_SRC}

doctest:
	${DOC_TEST}

docall: doc doctest


# TESTING
test:
	${PYTHON} -m unittest discover -v

testdoc:
	${PYTHON} -m test.test --doctests-only


# SERVER MANAGEMENT
# Notes for Linode
# (1) Use () syntax for subprocess,
# (2) leave off & to run in current terminal window.
# - Pushing & Serving
SERVE=cd webui/ && gunicorn --bind 0.0.0.0:5000 run:app \
	--access-logfile ../logs/access-logfile.log \
	--error-logfile ../logs/error-logfile.log \
	--capture-output \
	--pythonpath ../.venv/bin
serve-production-heroku:
	git checkout master && git branch -D production && git checkout -b production && git push trunk production -uf
serve-staging-heroku:
	git checkout develop && git branch -D staging && git checkout -b staging && git push trunk staging -uf
serve-production: serve-production-heroku
serve-staging: serve-staging-heroku
production: serve-production-heroku
staging: serve-staging-heroku
serve-production-linode:
	(${SERVE} --env APP_SETTINGS=production &)
serve-staging-linode:
	(${SERVE} --env APP_SETTINGS=staging &)
serve-local-flask:
	python webui/run.py
serve-heroku-local:
	heroku local
gunicorn:
	cd webui; \
	gunicorn -b 0.0.0.0:5000 run:app &
serve:gunicorn

# - SSH
production-connect-linode:
	ssh root@192.155.80.11
staging-connect-linode:
	ssh root@172.104.31.28

logs:
	heroku logs --app ppp-web
logs-staging:
	heroku logs --app ppp-web-staging

# - Dependency Management
ACTIVATE=source .venv/bin/activate
PIP=python -m pip install --upgrade git+https://github.com/
UPGRADE=${ACTIVATE} && ${PIP}

activate:
	${ACTIVATE}

add-remotes:
	git remote add trunk https://github.com/PMA-2020/ppp-web.git && \
	git remote add joeflack4 https://github.com/joeflack4/ppp-web.git

# CTAGS
tags:
	ctags -R --python-kinds=-i .

ltags:
	ctags -R --python-kinds=-i ./${CODE_SRC}

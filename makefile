#PYTHON=./env/bin/python3
PYTHON=python3
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


.PHONY: lint linttest lintall pylint pylinttest pylintall code codetest \
codeall doc doctest docall test testdoc serve serve-local serve-heroku-local \
serve-staging-linode serve-production-linode serve-production-heroku \
serve-production serve-staging-heroku serve-staging shell db production \
staging production-linode staging-linode tags ltags upgrade-pmix-trunk-master \
upgrade-pmix-trunk-develop upgrade-pmix-joeflack4-master \
upgrade-pmix-joeflack4-develop upgrade-pmix \
upgrade-ppp-web-joeflack4-develop upgrade-ppp-web activate upgrade-ppp \
serve-dev serve-dev-network-accessible production-connect-heroku \
staging-connect-heroku logs logs-staging production staging production-push \
 staging-push push-production push-staging circleci-validate-config


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
serve-dev-network-accessible:
	gunicorn --bind 0.0.0.0:5000 run:app \
	--access-logfile logs/access-logfile.log \
	--error-logfile logs/error-logfile.log \
	--capture-output \
	--pythonpath python3
serve:gunicorn
serve-dev: serve-local-flask
production-push:
	git status && \
	printf "\nGit status should have reported 'nothing to commit, working tree\
	 clean'. Otherwise you should cancel this command, make sure changes are\
	  committed, and run it again.\n\n" && \
	git checkout master && \
	git branch -D production && \
	git checkout -b production && \
	git push -u trunk production --force
staging-push:
	git status && \
	printf "\nGit status should have reported 'nothing to commit, working tree\
	 clean'. Otherwise you should cancel this command, make sure changes are\
	  committed, and run it again.\n\n" && \
	git checkout develop && \
	git branch -D staging && \
	git checkout -b staging && \
	git push -u trunk staging --force
push-production: production-push
push-staging: staging-push

# - SSH
production-connect-linode:
	ssh root@192.155.80.11
staging-connect-linode:
	ssh root@172.104.31.28
production-connect-heroku:
	heroku run bash --app ppp-web
staging-connect-heroku:
	heroku run bash --app ppp-web-staging
production: production-connect-heroku
staging: staging-connect-heroku

# - Logs
logs:
	heroku logs --app ppp-web
logs-staging:
	heroku logs --app ppp-web-staging

# - Devlops
circleci-validate-config:
	echo Make sure that Docker is running, or this command will fail. && \
	circleci config validate

# - Dependency Management
ACTIVATE=source .venv/bin/activate
PIP=python -m pip install --upgrade git+https://github.com/
UPGRADE=${ACTIVATE} && ${PIP}
activate:
	${ACTIVATE}
add-remotes:
	git remote add trunk https://github.com/PMA-2020/ppp-web.git && \
	git remote add joeflack4 https://github.com/joeflack4/ppp-web.git
upgrade-ppp:
	${PYTHON} -m pip uninstall odk-ppp && ${PYTHON} -m pip install \
	--no-cache-dir --upgrade odk-ppp

# CTAGS
tags:
	ctags -R --python-kinds=-i .
ltags:
	ctags -R --python-kinds=-i ./${CODE_SRC}

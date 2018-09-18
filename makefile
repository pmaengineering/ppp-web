SHELL=/bin/bash

.PHONY: lint linttest lintall pylint pylinttest pylintall code codetest \
codeall doc doctest docall test testdoc serve serve-local serve-heroku-local \
serve-staging-linode serve-production-linode push-production-heroku \
serve-production push-staging-heroku serve-staging shell db production \
staging production-linode staging-linode tags ltags upgrade-pmix-trunk-master \
upgrade-pmix-trunk-develop upgrade-pmix-joeflack4-master \
upgrade-pmix-joeflack4-develop upgrade-pmix upgrade-ppp-web-joeflack4-develop \
upgrade-ppp-web activate upgrade-ppp serve-dev serve-dev-network-accessible \
production-connect-heroku staging-connect-heroku logs logs-staging production \
staging production-push staging-push push-production push-staging \
circleci-validate-config update-ppp ppp-update ppp-upgrade gunicorn-local \
serve-local production-push-ci stagingpush-ci logs-heroku logs-staging-heroku \
validations validate git-hash git-hash install upgrade-once upgrade uninstall \
reinstall

# DEVELOPMENT
## Linting
SRC=./ppp_web/
TEST=./test/
### All linting
lint:
	${LINT_SRC}; ${CODE_SRC}; ${DOC_SRC}
linttest:
	${LINT_TEST}; ${CODE_TEST}; ${DOC_TEST}
lintall: lint linttest
### Pylint only
PYLINT=python3 -m pylint \
	--output-format=colorized \
	--reports=n
LINT_SRC=${PYLINT} ${SRC}
LINT_TEST=${PYLINT} ${TEST}
pylint:
	${LINT_SRC}
pylinttest:
	${LINT_TEST}
pylintall: pylint pylinttest
### Pycodestyle only
PYCODESTYLE=python3 -m pycodestyle
CODE_SRC=${PYCODESTYLE} ${SRC}
CODE_TEST=${PYCODESTYLE} ${TEST}
code:
	${CODE_SRC}
codetest:
	${CODE_TEST}
codeall: code codetest
### Pydocstyle only
PYDOCSTYLE=python3 -m pydocstyle
DOC_SRC=${PYDOCSTYLE} ${SRC}
DOC_TEST=${PYDOCSTYLE} ${TEST}
doc:
	${DOC_SRC}
doctest:
	${DOC_TEST}
docall: doc doctest

## Testing
test:
	python3 -m unittest discover -v
testdoc:
	python3 -m test.test --doctests-only

## Validations
circleci-validate-config:
	echo Make sure that Docker is running, or this command will fail.; \
	circleci config validate
validations: circleci-validate-config
validate: validations

# SERVERS & ENVIRONMENTS
GUNICORN=gunicorn ppp_web.ppp_web:app
## Local
serve-local-flask:
	python3 ppp_web/ppp_web.py
serve-heroku-local:
	heroku local
serve-dev-network-accessible:
	${GUNICORN} \
	--access-logfile logs/access-logfile.log \
	--error-logfile logs/error-logfile.log \
	--capture-output \
	--pythonpath python3
gunicorn-local: serve-dev-network-accessible

## Heroku
### Pushing & Serving
push-production-heroku:
	git status; \
	printf "\nGit status should have reported 'nothing to commit, working tree\
	 clean'. Otherwise you should cancel this command, make sure changes are\
	  committed, and run it again.\n\n"; \
	git checkout master; \
	git branch -D production; \
	git checkout -b production; \
	git push -u trunk production --force; \
	git checkout master; \
	open https://dashboard.heroku.com/apps/ppp-web/activity; \
	open https://circleci.com/gh/PMA-2020/workflows/ppp-web
push-staging-heroku:
	git status; \
	printf "\nGit status should have reported 'nothing to commit, working tree\
	 clean'. Otherwise you should cancel this command, make sure changes are\
	  committed, and run it again.\n\n"; \
	git checkout develop; \
	git branch -D staging; \
	git checkout -b staging; \
	git push -u trunk staging --force; \
	git checkout develop; \
	open https://dashboard.heroku.com/apps/ppp-web-staging/activity; \
	open https://circleci.com/gh/PMA-2020/workflows/ppp-web
production-push-heroku: push-production-heroku
staging-push-heroku: push-staging-heroku
production: push-production-heroku
staging: push-staging-heroku
serve-production:
	${GUNICORN}
serve-staging: serve-production
### SSH
production-connect-heroku:
	heroku run bash --app ppp-web
staging-connect-heroku:
	heroku run bash --app ppp-web-staging
### Logs
logs-heroku:
	heroku logs --app ppp-web
logs-staging-heroku:
	heroku logs --app ppp-web-staging

## Linode
### Notes
#   (1) Use () syntax for subprocess,
#   (2) leave off & to run in current terminal window.
### Pushing & Serving
SERVE=${GUNICORN} \
	--access-logfile ../logs/access-logfile.log \
	--error-logfile ../logs/error-logfile.log \
	--capture-output \
	--pythonpath ../.venv/bin
serve-production-linode:
	(${SERVE} --env APP_SETTINGS=production &)
serve-staging-linode:
	(${SERVE} --env APP_SETTINGS=staging &)
### SSH
production-connect-linode:
	ssh root@192.155.80.11
staging-connect-linode:
	ssh root@172.104.31.28
### Setup
ACTIVATE=source .venv/bin/activate
PIP=python -m pip install --upgrade git+https://github.com/
UPGRADE=${ACTIVATE}; ${PIP}
activate:
	${ACTIVATE}
add-remotes:
	git remote add trunk https://github.com/PMA-2020/ppp-web.git; \
	git remote add joeflack4 https://github.com/joeflack4/ppp-web.git

## Defaults
### Pushing & Serving
serve: serve-local-flask
production-push-ci: production-push-heroku
staging-push-ci: staging-push-heroku
production-push: production-push-ci
staging-push: staging-push-ci
push-production: production-push
push-staging: staging-push
gunicorn: serve-production
serve-local: serve
serve-dev: serve-local-flask
### SSH
production-connect: production-connect-heroku
staging-connect: staging-connect-heroku
### Logs
logs: logs-heroku
logs-staging: logs-staging-heroku
### Dependency Management
# For some reason, if something has been uploaded to pip very recently, you
# need to --upgrade using --no-cache-dir.
git-hash:
	git rev-parse --verify HEAD
install:
	pip install -r requirements-unlocked.txt --no-cache-dir; \
	pip freeze > requirements.txt; \
	make upgrade-once
upgrade-once:
	pip install -r requirements-unlocked.txt --no-cache-dir --upgrade; \
	pip freeze > requirements.txt
upgrade:
	make upgrade-once; \
	make upgrade-once
uninstall:
	workon ppp-web; \
	bash -c "pip uninstall -y -r <(pip freeze)"
reinstall:
	make uninstall; \
	make install; \
	make upgrade

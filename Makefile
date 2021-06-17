include ./Makefile.in.mk


.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
#	$(RUN) isort --virtual-env="$(DIR_VENV)" "$(DIR_SRC)" "$(DIR_SCRIPTS)" "$(DIR_TESTS)"
	$(RUN) black "$(DIR_SRC)" "$(DIR_SCRIPTS)" "$(DIR_TESTS)"


.PHONY: test
test:
	$(call log, running tests)
	$(RUN) pytest
#	$(RUN) isort --virtual-env="$(DIR_VENV)" --check-only "$(DIR_SRC)" "$(DIR_SCRIPTS)" "$(DIR_TESTS)"
	$(RUN) black --check "$(DIR_SRC)" "$(DIR_SCRIPTS)" "$(DIR_TESTS)"


.PHONY: run
run:
	$(call log, starting local api server)
	$(RUN) uvicorn main:app --reload


.PHONY: run-prod
run-prod:
	$(call log, starting local web server)
	$(RUN) uvicorn src.main:app --reload


.PHONY: venv
venv:
	$(call log, installing packages)
	$(PIPENV_INSTALL)


.PHONY: venv-dev
venv-dev:
	$(call log, installing development packages)
	$(PIPENV_INSTALL) --dev


.PHONY: pycharm
pycharm:
	$(call log, setting pycharm up)
	$(PYTHON) $(DIR_SCRIPTS)/setup_pycharm.py


.PHONY: dropdb
dropdb:
	$(call log, dropping database)
	psql \
		--echo-all \
		--username=$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_user.py) \
		--no-password \
		--host=localhost \
		--dbname=postgres \
		--command="DROP DATABASE IF EXISTS \"$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py)\";"


.PHONY: createdb
createdb:
	$(call log, creating database)
	psql \
		--echo-all \
		--username=$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_user.py) \
		--no-password \
		--host=localhost \
		--dbname=postgres \
		--command="CREATE DATABASE \"$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py)\";"

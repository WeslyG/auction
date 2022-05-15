.PHONY: deps test

deps:
	pip install -r req.txt

init_db: deps
	python init_db.py

run: init_db
	flask run

dev_run:
	FLASK_APP=app FLASK_ENV=development flask run
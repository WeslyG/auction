.PHONY: deps test

deps:
	pip install -r req.txt

init_db: deps
	python init_db.py

run: init_db
	python server.py

dev_run:
	FLASK_APP=server FLASK_ENV=development flask run
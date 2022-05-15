.PHONY: deps run dev_run

deps:
	pip install -r req.txt

run: deps
	flask run

dev_run:
	FLASK_APP=app FLASK_ENV=development flask run
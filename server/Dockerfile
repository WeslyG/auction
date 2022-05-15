FROM python:3.9.12-slim

WORKDIR /app

COPY req.txt req.txt

RUN pip3 install -r req.txt

COPY . .

RUN python init_db.py

EXPOSE 5000
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
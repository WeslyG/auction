from app import app

@app.route("/", methods =['GET'])
def hey():
    return '{ "status": "ok" }'
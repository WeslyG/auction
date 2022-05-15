
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import  check_password_hash, generate_password_hash
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'CZc4J6iUr~xhX2A%W5DD'

login_manager = LoginManager(app)


# TODO: https://pypi.org/project/flask-crontab/

#####MODELS#######

from src.models.user import User
from src.models.lot import Lot
from src.models.queue import Queue

#####SCHEMA########

from src.schema.user import UserSchema
from src.schema.lot import LotSchema
from src.schema.queue import QueueSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
lot_schema = LotSchema()
lots_schema = LotSchema(many=True)
queue_schema = QueueSchema()
queues_schema = QueueSchema(many=True) 

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
    # return User.query.get(user_id)

######API###########

import src.routes.init

#АВТОРИЗАЦИЯ
@app.route("/login", methods =['POST'])
def login():
    new_user_data = json.loads(request.data)
    user = db.session.query(User).filter(User.login == new_user_data['login']).first()
    # id = str(user.id)
    if user and check_password_hash(user.password, new_user_data['password']):
        # response = make_response("Setting a cookie")
        # response.set_cookie( 'id', '2', max_age=60*60*24*365*2)
        if login_user(user):
            return 'Ok'
        # response = make_response('')
        # response.set_cookie('id', id, 60*60*24*15)
    else:
        return 'not ok'


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(somewhere)


##РЕГИСТРАЦИЯ
@app.route("/register", methods=['GET', 'POST'])
def register():
    req_fields = ["name", "password", "login"]
    if request.method == 'POST':
        new_user_data = json.loads(request.data)
        for key in new_user_data.keys():
            if key not in req_fields:
                resp = { "message": f"{key} is required"}
                return jsonify(resp), 403
        hash = generate_password_hash(new_user_data['password'])
        new_user = User(name=new_user_data['name'], login=new_user_data['login'], password=hash)
        db.session.add(new_user)
        db.session.commit()
        return "", 201
    else:
        user = User.query.all()
        result =  users_schema.dump(user, many=True)
        return {'users': result}

##СОЗДАНИЕ ЛОТА
@app.route('/lot', methods=['GET'])
@login_required
def get_all_lots():
    lot = Lot.query.all()
    return jsonify(lots_schema.dump(lot, many=True))

@app.route('/lot', methods=['POST'])
@login_required
def create_lot():
    body = json.loads(request.data)
    id_user = int(session['_user_id'])
    new_lot = Lot(id_author=id_user, name=body['name'], description=body['description'], price=body['price'])
    db.session.add(new_lot)
    db.session.commit()
    return lot_schema.dump(new_lot)


##ПОЛУЧЕНИЕ ЛОТОВ КОТОРЫЕ ПРОДАЕТ ЮЗЕР
@app.route('/lot/my', methods=['GET'])
@login_required
def get_my_lots():
    id_user = int(session['_user_id'])
    lots = db.session.query(Lot).filter(Lot.id_author == id_user)
    return jsonify(lots_schema.dump(lots, many=True))


##ПОЛУЧЕНИЕ ВСЕХ ЛОТОВ ДРУГИХ ЮЗЕРОВ 
@app.route('/lot/other', methods=['GET'])
@login_required
def get_lots():
    id_user = int(session['_user_id'])
    lots = db.session.query(Lot).filter(Lot.id_author != id_user)
    return jsonify(lots_schema.dump(lots, many=True))

#ПОЛУЧЕНИЕ ЛОТОВ КОТОРЫЕ ХОЧЕТ ПРЕОБРЕСТИ ЮЗЕР 
@app.route('/lot/withlist', methods =['GET'])
@login_required
def want_buy():
    id_user = int(session['_user_id'])
    lots = db.session.query(Queue).filter(Queue.id_buyer == id_user)
    return jsonify(queues_schema.dump(lots, many=True))


@app.route('/lot/<int:id_lot>', methods =['GET'])
@login_required
def show_one_lot(id_lot):
    id_user = int(session['_user_id'])
    lot = db.session.query(Lot).filter(Lot.id == id_lot)
    print('=============')
    print(lot.name)
    return 'kkk'
    # print(lot['time'])
    # print(lot.time)


#ВСТАТЬ В ОЧЕРЕДЬ ЛОТА
@app.route('/lot/<int:id_lot>', methods =['POST']) ## <int:id_lot>
@login_required
def buy_lot(id_lot):
    id_user = int(session['_user_id'])
    now = datetime.now()
    print(datetime.now().isoformat())
    lot = db.session.query(Lot).filter(Lot.id == id_lot).update({ "date_time": datetime.now().isoformat() })
    db.session.commit()

    return jsonify(lot)
    lot = db.session.query(Lot).filter(Lot.id == id_lot)
    lot_obj = lot_schema.dumps(lot)


    # if lot.time == datetime(1,1,1):
    #     lot.time = time_now
    #     end_queue = Queue(id_lot=id_lot, id_buyer=id_user, date_time=time_now)
    #     db.session.add(end_queue)
    #     db.session.commit()
    #     return 'OK'
    # elif request.args['increase'] > 0 and lot.time + timer < datetime.now():
    #     lot.price = lot.price + request.args['increase']
    #     lot.time = time_now
    #     end_queue = Queue(id_lot=id_lot, id_buyer=id_user, date_time=time_now)
    #     db.session.add(end_queue)
    #     db.session.commit()
    #     return 'OK'
    # else: 
    #     winner = db.session.query(Queue).filter(Queue.id_lot == id_lot)[-1]
    #     return 'лот пренадлежит ', winner.id_buyer

    # else: 
    #     if lot.time + timer >= datetime.now():
    #         return 'Лот продан'
    #     else:
    #         return 'Лот еще открыт'


if __name__ == "__main__":
    db.create_all()
    app.run()
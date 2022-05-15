
from datetime import datetime, timedelta
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import  check_password_hash, generate_password_hash

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
from src.schema.product import ProductSchema
from src.schema.queue import QueueSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
queue_schema = QueueSchema()
queues_schema = QueueSchema(many=True) 

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
    # return User.query.get(user_id)

######API###########

import src.routes.init

#АВТОРИЗАЦИЯ
@app.route("/login", methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(User).filter(User.login == request.args['login']).first()
        # id = str(user.id)
        if user and check_password_hash(user.password, request.args['password']):  
            # response = make_response("Setting a cookie")
            # response.set_cookie( 'id', '2', max_age=60*60*24*365*2)
            if login_user(user):
                return 'Ok'
            # response = make_response('')
            # response.set_cookie('id', id, 60*60*24*15)
            return 'ОК' #, response


        # else:
        #     print(session[id])
        #     return 'неверный логин или пороль' #  users_schema.dump(User.query.all())




# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(somewhere)


##РЕГИСТРАЦИЯ 
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.args['password'] == request.args['password2']:
            hash = generate_password_hash(request.args['password'])
            new_user = User(name=request.args['name'], login=request.args['login'], password=hash)
            db.session.add(new_user)
            db.session.commit()
            return 'OK'
        else:
            return 'нет данных'
    else:
        user = User.query.all()
        result =  users_schema.dump(user, many=True)
        return {'users': result}
    



##СОЗДАНИЕ ЛОТА
@app.route('/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot():
    if request.method == 'POST':
        id_auth = int(session['_user_id'])
        print(id_auth)
        name_lot = request.args['name']
        description_lot = request.args['description']
        price_lot = request.args['price']
        new_lot = Lot(id_author=id_auth, name=name_lot, description=description_lot, price=price_lot, time=datetime(1,1,1))
        db.session.add(new_lot)
        db.session.commit()
        return 'OK'
    else:
        # current_user.is_authenticated
        # result = current_user.id()
        # result = User.get_id()
        lot = Lot.query.all()
        result =  products_schema.dump(lot, many=True)
        return {'lots': result}




##ПОЛУЧЕНИЕ ЛОТОВ КОТОРЫЕ ПРОДАЕТ ЮЗЕР
@app.route('/get_my_lots', methods=['GET', 'POST'])
@login_required
def get_my_lots():
    id_user = int(session['_user_id'])
    lots = db.session.query(Lot).filter(Lot.id_author == id_user)
    result = products_schema.dump(lots, many=True)
    return {'lots': result}


##ПОЛУЧЕНИЕ ВСЕХ ЛОТОВ ДРУГИХ ЮЗЕРОВ 
@app.route('/get_lots', methods=['GET', 'POST'])
@login_required
def get_lots():
    id_user = int(session['_user_id'])
    lots = db.session.query(Lot).filter(Lot.id_author != id_user)
    result = products_schema.dump(lots, many=True)
    return {'lots': result}

#ПОЛУЧЕНИЕ ЛОТОВ КОТОРЫЕ ХОЧЕТ ПРЕОБРЕСТИ ЮЗЕР 
@app.route('/want_buy', methods =['GET', 'POST'])
@login_required
def want_buy():
    id_user = int(session['_user_id'])
    lots = db.session.query(Queue).filter(Queue.id_buyer == id_user)
    result = queues_schema.dump(lots, many=True)
    return {'lots': result}


#ВСТАТЬ В ОЧЕРЕДЬ ЛОТА
@app.route('/buy_lot/<int:id_lot>', methods =['GET', 'POST']) ## <int:id_lot>
# @login_required
def buy_lot(id_lot):
    # timer = datetime.timedelta(hours=24)
    id_lott = 2
    timer = timedelta(minutes=2)
    id_user = int(session['_user_id'])
    if request.method == 'POST':
        lots = db.session.query(Lot).filter(Lot.id == id_lott)
        result = products_schema.dump(lots, many=True)
        return {'lots': result}

    #     if lot.time == datetime(1,1,1):
    #         lot.time = time_now
    #         end_queue = Queue(id_lot=id_lot, id_buyer=id_user, date_time=time_now)
    #         db.session.add(end_queue)
    #         db.session.commit()
    #         return 'OK'
    #     elif request.args['increase'] > 0 and lot.time + timer < datetime.now():
    #         lot.price = lot.price + request.args['increase']
    #         lot.time = time_now
    #         end_queue = Queue(id_lot=id_lot, id_buyer=id_user, date_time=time_now)
    #         db.session.add(end_queue)
    #         db.session.commit()
    #         return 'OK'
    #     else: 
    #         winner = db.session.query(Queue).filter(Queue.id_lot == id_lot)[-1]
    #         return 'лот пренадлежит ', winner.id_buyer

    # else: 
    #     if lot.time + timer >= datetime.now():
    #         return 'Лот продан'
    #     else:
    #         return 'Лот еще открыт'

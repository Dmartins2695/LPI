import base64
import datetime
import os
import sqlalchemy
from datetime import datetime
from functools import wraps

import jwt
from flask import Flask, render_template, request, make_response, jsonify, redirect, g
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
app.secret_key = '%tY24$iKao@£Po&'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lolada123@localhost/LPI'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'q2W£e4R§'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

    # cria todas as tabelas


@app.before_first_request
def create_tables():
    db.create_all()


# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return RevokedTokenModel.is_jti_blacklisted(jti)


# DATABASE SECTION

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # verifica se ja existe algum utilizador com esse username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # @classmethod
    # def find_by_email(cls, email):
    #  return cls.query.filter_by(email=email).first()

    @classmethod
    def find_images_by_id(cls, id):
        return ImageModel.find_images_by_id(id)

    # retorna todos os utilizadores
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    # elimina todos os utilizadores
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

            # para gerar hash

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    # para verificar hash no login
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserLogin(Resource):
    def post(self):
        parser_login = parser.copy()
        parser_login.add_argument('username', help='This field cannot be blank', required=False)
        parser_login.add_argument('password', help='This field cannot be blank', required=False)
        data = parser_login.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
                'message': 'Wrong credentials',
                'access_token': "error",
                'code': 'user_not_exists'
            }

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'code': 'login_with_fields'
            }
        else:
            return {
                'message': 'Wrong credentials',
                'access_token': "error",
                'code': 'wrong_credentials'
            }


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route('/student/<id>')
def hello_world(id):
    return 'Hello,' + id

    # IMAGE PROCESSING SeCTION


class receiveImage(Resource):
    def post(self):
        path = "C:\\Users\danie\PycharmProjects\Cliente\\venv\serverImages"
        parser_upload = parser.copy()
        parser_upload.add_argument('image', help='Image cannot be blank', required=False)
        data = parser_upload.parse_args()
        image = data['image']
        bytes = base64.b64decode(image)
        date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(path + "\\" + date + '.jpg', "wb") as img:
            img.write(bytes)
            print(img.name)
        return 200


api.add_resource(receiveImage, '/receiveImage', endpoint="receiveImage")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="192.168.1.81", port="5000")
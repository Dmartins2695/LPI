import base64
import datetime
import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, make_response, jsonify, redirect, g, url_for, session, logging, flash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lolada123@localhost/LPI'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '%tY24$iKao@£Po&'
jwt = JWTManager(app)


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing Token'}), 403
        try:
            data: jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': ' Invalid token'}), 403
        return func(*args, **kwargs)

    return wrapped

    # cria todas as tabelas


@app.before_first_request
def create_tables():
    db.create_all()


# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return RevokedTokenModel.is_jti_blacklisted(jti)


# DATABASE SECTION

class studentModel(db.Model):
    __tablename__ = 'students'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    username = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

# verifica se ja existe algum utilizador com esse email

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

# verifica se ja existe algum utilizador com esse username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    # para verificar hash no login
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    # # client login
    # class UserLogin(Resource):
    #     def post(self):
    #         parser_login = parser.copy()
    #         parser_login.add_argument('username', help='This field cannot be blank', required=False)
    #         parser_login.add_argument('password', help='This field cannot be blank', required=False)
    #         data = parser_login.parse_args()
    #         current_user = UserModel.find_by_username(data['username'])
    #         if not current_user:
    #             return {
    #                 'message': 'Wrong credentials',
    #                 'access_token': "error",
    #                 'code': 'user_not_exists'
    #             }
    #
    #         if UserModel.verify_hash(data['password'], current_user.password):
    #             access_token = create_access_token(identity=data['username'])
    #             refresh_token = create_refresh_token(identity=data['username'])
    #             return {
    #                 'message': 'Logged in as {}'.format(current_user.username),
    #                 'access_token': access_token,
    #                 'refresh_token': refresh_token,
    #                 'code': 'login_with_fields'
    #             }
    #         else:
    #             return {
    #                 'message': 'Wrong credentials',
    #                 'access_token': "error",
    #                 'code': 'wrong_credentials'
    #             }


    # retorna todos os utilizadores
    # @classmethod
    # def return_all(cls):
    #     def to_json(x):
    #         return {
    #             'username': x.username,
    #             'password': x.password
    #         }
    #
    #     return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

class UserModel(db.Model):
    __tablename__ = 'users'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # verifica se ja existe algum utilizador com esse email
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # verifica se ja existe algum utilizador com esse username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # @classmethod
    # def find_images_by_id(cls, id):
    #     return ImageModel.find_images_by_id(id)


    # # elimina todos os utilizadores
    # @classmethod
    # def delete_all(cls):
    #     try:
    #         num_rows_deleted = db.session.query(cls).delete()
    #         db.session.commit()
    #         return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    #     except:
    #         return {'message': 'Something went wrong'}

    # para gerar hash

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    # para verificar hash no login
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


# Web app side
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form.get("user")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        client = UserModel(username=user, email=email, password=UserModel.generate_hash(password))

        if client.find_by_email(email):
            flash('Este email já foi registrado, tente um novo!', 'danger')
            return render_template('register.html')

        elif client.find_by_username(user):
            flash('User já existe, tente um novo!', 'danger')
            return render_template('register.html')

        elif password != confirm:
            flash('Palavra passe errada, tente novamente!', 'danger')
            return render_template('register.html')

        else:
            client.save_to_db()
            flash('Registro efetuado com sucesso!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/room')
def room():
    if request.method == "GET":
        header = session['code']
    else:
        return render_template('home.html')
    return render_template('room.html', messages=header)


@app.route('/createRoom', methods=["GET", "POST"])
def createRoom():
    if request.method == "POST":
        rname = request.form.get("roomname")
        code = rname + datetime.now().strftime("%d%m%Y%H%M%S")
        session['code'] = code
        flash('Sala criada com successo!', 'success')
        return redirect(url_for('room'))
    else:
        return render_template("createRoom.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        if UserModel.find_by_username(user) is None:
            flash('User ou password errada, tente novamente!', 'danger')
            return render_template('login.html')
        else:
            client = UserModel.find_by_username(user)
            if UserModel.verify_hash(password, client.password):
                session["user"] = user
                # token = jwt._create_access_token({
                #     'user': user,
                #     'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                # },
                # app.config['SECRET_KEY'])
                # session['token']=token
                flash('Login efetuado com successo!', 'success')
                return redirect(url_for('user'))
    else:
        if "user" in session:
            redirect(url_for('user'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))


@app.route('/user')
# @check_for_token
def user():
    name = session['user']
    return render_template('user.html', messages=name)

    # IMAGE PROCESSING SeCTION


@app.route('/check', methods=['GET'])
def checkCode(data):
    if data == session['code']:
        return 200
    else:
        return 404


class receiveCode(Resource):
    def post(self):
        parser_upload = parser.copy()
        parser_upload.add_argument('roomCode', help='code cannot be blank', required=False)
        data = parser_upload.parse_args()
        code = data['roomCode']
        print(code)
        return redirect(url_for('check', _method='GET', data=code)), 200


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
api.add_resource(receiveCode, '/receiveCode', endpoint="receiveCode")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="192.168.1.99", port="5000")

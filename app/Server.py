import base64
import datetime
import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_jwt_extended import (
    JWTManager
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
# IMAGE_FOLDER = os.path.join('static', 'serverImages')
# app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
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


class RoomModel(db.Model):
    __tablename__ = 'roomsCreated'

    def __init__(self, roomName, code, owner):
        self.roomName = roomName
        self.code = code
        self.owner = owner

    roomName = db.Column(db.String(120), unique=True, nullable=False)
    code = db.Column(db.String(150), primary_key=True, unique=True, nullable=False)
    owner = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_roomName(cls, roomName):
        return cls.query.filter_by(roomName=roomName).first()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_owner_Rooms(cls, owner):
        return cls.query.filter_by(owner=owner)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    # para verificar hash no login
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    # elimina todos os utilizadores
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


class ImageModel(db.Model):
    __tablename__ = 'images'

    def __init__(self, username, image):
        self.username = username
        self.image = image

    image = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # verifica se ja existe algum utilizador com esse email

    @classmethod
    def find_by_image(cls, image):
        return cls.query.filter_by(image=image).first()

    @classmethod
    def find_allImages(cls, username):
        return cls.query.filter(cls.username == username)

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

    @classmethod
    def find_images_by_id(cls, id):
        return ImageModel.find_images_by_id(id)

    # elimina todos os utilizadores
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


class StudentModel(db.Model):
    __tablename__ = 'students'

    def __init__(self, username, email, password, status):
        self.username = username
        self.email = email
        self.password = password
        self.status = status

    username = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).first()

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

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

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

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    # para verificar hash no login
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


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


@app.route('/showStudentImages/<studentName>', methods=["GET", "POST"])
def showStudentImages(studentName):
    if request.method == "GET":  # como por imagens na web
        allImages = ImageModel.find_allImages(studentName)
        for image in allImages:
            print(image.image)
        return render_template('showStudentImages.html', allImages=allImages, studentName=studentName)


@app.route('/listRooms', methods=["GET", "POST"])
def listRooms():
    user = session['user']
    ownedRooms = RoomModel.find_owner_Rooms(user)
    return render_template('listRooms.html', ownedRooms=ownedRooms)


@app.route('/room/<name>', methods=["GET", "POST"])
def room(name):
    if request.method == "POST":
        studentName = request.form.get("studentName")
        return redirect(url_for('showStudentImages', studentName=studentName))
    else:
        return redirect(url_for('room', name=name))


@app.route('/createRoom', methods=["GET", "POST"])
def createRoom():
    if request.method == "POST":
        rname = request.form.get("roomname")
        code = rname + datetime.now().strftime("%d%m%Y%H%M%S")
        user = session['user']
        room = RoomModel(rname, code, user)
        room.save_to_db()
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


class studentLogin(Resource):
    def post(self):
        parser_upload = parser.copy()
        parser_upload.add_argument('StudentUser', help='code cannot be blank', required=False)
        parser_upload.add_argument('StudentPassword', help='code cannot be blank', required=False)
        data = parser_upload.parse_args()
        user = data['StudentUser']
        password = data['StudentPassword']

        client = StudentModel.find_by_username(user)
        print(client.email)
        if StudentModel.verify_hash(password, client.password):
            session['Studentuser'] = user
            return {'code': 'sucess'}
        else:
            return {'code': 'wrong_credentials'}


class studentRegister(Resource):
    def post(self):
        parser_upload = parser.copy()
        parser_upload.add_argument('StudentUser', help='code cannot be blank', required=False)
        parser_upload.add_argument('StudentPassword', help='code cannot be blank', required=False)
        parser_upload.add_argument('StudentEmail', help='code cannot be blank', required=False)
        data = parser_upload.parse_args()
        username = data['StudentUser']
        password = data['StudentPassword']
        email = data['StudentEmail']
        client = StudentModel(username=username, email=email, password=StudentModel.generate_hash(password),
                              status=' false')
        client.save_to_db()
        return 200


class receiveCode(Resource):
    def post(self):
        parser_upload = parser.copy()
        parser_upload.add_argument('roomCode', help='code cannot be blank', required=False)
        data = parser_upload.parse_args()
        code = data['roomCode'] # receber user name mudar status
        room = RoomModel.find_by_code(code)
        if code == room.code:
            return {'code': 'sucess'}
        else:
            return {
                'code': 'error',
                'message': 'room not found'
            }


class receiveImage(Resource):
    def post(self):
        path = "C:\\Users\danie\PycharmProjects\SuperViser\\venv\\app\serverImages"
        parser_upload = parser.copy()
        parser_upload.add_argument('image', help='Image cannot be blank', required=False)
        #  parser_upload.add_argument('StudentUser', help='code cannot be blank', required=False)
        data = parser_upload.parse_args()
        image = data['image']
        # user = data['StudentUser']
        # client = StudentModel.find_by_username(user)
        bytes = base64.b64decode(image)
        date = datetime.now().strftime("%d%m%Y_%H%M%S")
        imagepath = path + "\\" + '_' + date + '.jpg'  # missing + client.username
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(imagepath, "wb") as img:
            img.write(bytes)
        # imgtosave = ImageModel(username=client.username, image=imagepath)
        # imgtosave.save_to_db()
        return 200


api.add_resource(receiveImage, '/receiveImage', endpoint="receiveImage")
api.add_resource(receiveCode, '/receiveCode', endpoint="receiveCode")
api.add_resource(studentLogin, '/studentLogin', endpoint="studentLogin")
api.add_resource(studentRegister, '/studentRegister', endpoint="studentRegister")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="192.168.1.99", port="5000")

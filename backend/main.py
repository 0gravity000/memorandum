from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import json
from google.cloud import datastore
from datetime import date, datetime
#from model import User, Bookmark, Tag, BookmarkUser, BookmarkTag
from bookmarks import bookmarks_bp
from tags import tags_bp
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import re

# instantiate the app
app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
#app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(bookmarks_bp)
app.register_blueprint(tags_bp)
# flask_login関連
login_manager = LoginManager()  # ログインマネージャーインスタンスを作成
login_manager.init_app(app)
secret = secrets.token_urlsafe(32)  # flask_login ランダムなセッションを生成
app.secret_key = secret
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
# LEVEL を DEBUG に変更
logging.basicConfig(level=logging.DEBUG)
# Instantiates a client
client = datastore.Client()

# Flask-login ###############################
# user_loaderコールバックを提供する必要があります。 
# このコールバックは、セッションに保存されているユーザーIDからユーザーオブジェクトをリロードするために使用されます。 
# ユーザーのstr IDを取得し、対応するユーザーオブジェクトを返す必要があります。
@login_manager.user_loader
def load_user(user_id):  #userをロードするためのcallback functionを定義
    # ？load_userの引数は、Userクラス？で定義したget_id()が返す値です。
    # これはstrでなければならないことに注意してください。
    # ？user_idはユーザーテーブルの主キーにすぎないため、ユーザーのクエリで使用します
    logging.debug('now in load_user')
    user = User()   
    logging.debug(user)
    return user #認証されたユーザを特定するインスタンス
    #return user.id #これはダメ。インスタンスを返さないとダメ

@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    json = request.get_json()
    logging.debug(json)
    user = User()
    # データストアに登録
    return jsonify(user.registet_user())

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    json = request.get_json()
    logging.debug(json)
    user = User()
    rtn = user.login_user()
    # Flask-loginのログイン処理
    login_user(user)    #★login_user 関数を使用してログインする
    return jsonify(rtn)

@app.route('/api/auth/logout', methods=['GET'])
def auth_logout():
    # Flask-loginのログアウト処理
    logout_user()
    # Userクラスのクラスプロパティをクリア
    User.id = None
    User.email = None
    User.password = None
    User.nickname = None

    return "logout"

class User(UserMixin): # UserMixinを継承 Flask-Loginの属性をモデルに追加
    id = None
    email = None
    password = None
    nickname = None
    created_at = None
    updated_at = None
    def __init__(self):
        pass

    def get_id(self):
        """
        UserMixinを継承 メソッド get_id()
        このメソッドは、このユーザーを一意に識別するstrを返す必要があり、
        user_loaderコールバックからユーザーをロードするために使用できます。
        これはstrでなければならないことに注意してください。
        IDがネイティブにintまたはその他の型である場合は、strに変換する必要があります。
        https://flask-login.readthedocs.io/en/latest/_modules/flask_login/mixins/#UserMixin
        """
        logging.debug('now User get_id')
        logging.debug(User.id)
        return (User.id)

    def registet_user(self):
        logging.debug('now in register user')
        json = request.get_json()
        logging.debug(json)
        # The kind for the new entity
        kind = "User"
        # The name/ID for the new entity
        # 重複チェック
        query = client.query(kind=kind)
        result = list(query.add_filter('email', '=', json["email"]).fetch())
        if result:
            return "Already registered"

        # The Cloud Datastore key for the new entity
        user_key = client.key(kind)
        # Prepares the new entity
        user = datastore.Entity(key=user_key)
        user["email"] = json["email"]
        user["password"] = generate_password_hash(json["password"], method='sha256')
        user["nickname"] = json["nickname"]
        user["updated_at"] = datetime.utcnow()
        user["created_at"] = datetime.utcnow()
        logging.debug(user)
        # Saves the entity
        client.put(user)
        #userid = user.key.id
        #logging.debug(userid)
        logging.debug('now leave register user')
        return user

    def login_user(self):
        logging.debug('now in login user')
        json = request.get_json()
        logging.debug(json)
        # バリデーション
        #emailアドレスの空白チェック
        if json["email"] == None:
            return "email empty"
        #パスワードの空白チェック
        if json["password"] == None:
            return "password empty"
        #有効なemailアドレスかチェック
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        #pattern = "^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]+.[A-Za-z0-9]+$"
        if not re.match(pattern, json["email"]):
            return "email invalid"

        # The kind for the new entity
        kind = "User"
        # The name/ID for the new entity
        query = client.query(kind=kind)
        result = list(query.add_filter('email', '=', json["email"]).fetch())
        logging.debug(result)
        if not result:
            return "no user"

        logging.debug(result[0])
        user = result[0]
        # 複数itemになる場合はないはず。（複数itemになったらこれはダメ）
        # for user in result:
        #     #user = dict(item)
        #     logging.debug('★★★')
        #     logging.debug(user)
        #     #パスワードの一致チェック
        #     if not check_password_hash(user["password"], json["password"]):
        #         return "password not match"

        User.id = user.key.id
        User.email = json["email"]
        User.password = generate_password_hash(json["password"], method='sha256')
        User.nickname = json["nickname"]

        logging.debug('now leave login user')
        return user

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

@app.route('/api/adjustBookmark', methods=['POST'])
def adjust_bookmark():
    json = request.get_json()
    #logging.debug(json)
    beforeBookmark = json["beforeBookmark"]
    #logging.debug(beforeBookmark)
    soup = BeautifulSoup(beforeBookmark, "html.parser")
    # logging.debug(soup)
    #txt = soup.get_text()
    hrefs = []
    # logging.debug(soup.find_all('a'))
    for tag in soup.find_all(["a", "h3"]):
        #logging.debug(tag)
        hrefs.append({'name': tag.name, 'txt': tag.string, 'href': tag.get('href')})
    return jsonify(hrefs)


@app.route('/api/stroke/ahref', methods=['POST'])
def stroke_ahref():
    json = request.get_json()
    logging.debug(json)
    url = json["targetUrl"]
    logging.debug(url)
    #url = "https://example.com"
    res = requests.get(url)
    # logging.debug(res.content)
    soup = BeautifulSoup(res.content, "html.parser")
    # logging.debug(soup)
    #txt = soup.get_text()
    hrefs = []
    allText = ""
    # logging.debug(soup.find_all('a'))
    for link in soup.find_all('a'):
        # logging.debug(link)
        # logging.debug(link.string)
        hrefs.append({'href': link.get('href'), 'txt': link.string})
    allText = soup.get_text("｜")
    # logging.debug(hrefs)
    return jsonify(hrefs, allText)


@app.route('/api/books', methods=['GET'])
def all_books():
    return jsonify({
        'status': 'success',
        'books': BOOKS
    })


@app.route("/api/ping")
def hello_world():
    return jsonify('pong!')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=('GET', 'POST'))
def index(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

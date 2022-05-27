from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import json
from google.cloud import datastore
from datetime import date, datetime, timedelta
#from model import User, Bookmark, Tag, BookmarkUser, BookmarkTag
from bookmarks import bookmarks_bp
from tags import tags_bp
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import re
from common import add_keyid_queryresult
from users import User

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
    logging.debug('now in login user')
    # セッションのタイムアウト設定
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    user = User()
    rtnuser = user.login_user()
    # Flask-loginのログイン処理
    login_user(user)    #★login_user 関数を使用してログインする
    logging.debug(current_user.email)
    logging.debug(current_user.id)

    # idを付加する    
    user_with_id = dict(rtnuser)
    user_with_id["id"] = rtnuser.key.id
    logging.debug(user_with_id)
    logging.debug('now leave login user')

    return jsonify(user_with_id)

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

@app.route('/api/auth/check', methods=['GET'])
def auth_check():
    logging.debug('now in auth_check')
    logging.debug(current_user.is_authenticated)
    if not current_user.is_authenticated:
        user = {"id": "", "email": "ゲスト", "password": "", "nickname": ""}
        return user

    user = User()
    rtnuser = user.get_current_user_obj()
    # key = client.key("User", int(current_user.id))
    # user = client.get(key)
    # logging.debug('now leave auth_check')
    return rtnuser


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

    allText = soup.get_text("｜", strip=True)
    #allText = [text for text in soup.stripped_strings] #NG
    #allText = soup.get_text("｜")
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

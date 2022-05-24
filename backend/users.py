from flask import Flask, jsonify, render_template, request, Blueprint
import logging
import json
from google.cloud import datastore
from datetime import date, datetime
from common import add_keyid_queryresult
from bookmark_tags import BookmarkTags
#from bookmark_tags import BookmarkTags, show_bookmark_tags, update_bookmark_tags
from tags import Tag
from bookmark_users import BookmarkUsers
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bookmark_tags import BookmarkTags
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Instantiates a client
client = datastore.Client()

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
        logging.debug(str(User.id))
        return (str(User.id))

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
        # パスワードの一致チェック
        if not check_password_hash(user["password"], json["password"]):
            return "password not match"
        # Userクラスのクラスプロパティに値をセット
        User.id = user.key.id
        User.email = user["email"]
        User.password = user["password"]
        User.nickname = user["nickname"]
        logging.debug(User.id)
        # User.email = json["email"]
        # User.password = generate_password_hash(json["password"], method='sha256')
        # User.nickname = json["nickname"]
        return user

    def get_current_user_obj(self):
        user = {
            'id': User.id,
            'email': User.email,
            'password': User.password,
            'nickname': User.nickname,
        }
        return user

    def get_users(self):
        logging.debug('now in get users')
        # The kind for the new entity
        kind = "User"
        query = client.query(kind=kind)
        #logging.debug(query)
        result = list(query.fetch())
        #logging.debug(result)
        if not result:
            logging.debug('now leave get tags')
            return ""
        users = add_keyid_queryresult(result)
        logging.debug('now leave get users')
        return users

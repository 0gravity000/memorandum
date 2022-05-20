from flask import Flask, jsonify, render_template, request
import logging
import json
from google.cloud import datastore
from datetime import date, datetime

from flask import Blueprint

# Instantiates a client
client = datastore.Client()

# Blueprintオブジェクトを生成
bookmarks_bp = Blueprint('bookmarks', __name__, url_prefix='/api/bookmarks')

@bookmarks_bp.route('/', methods=['GET', 'POST'])
def bookmarks():
    if request.method == 'POST':    #POST Method
        logging.debug('now in post bookmarks')
        json = request.get_json()
        logging.debug(json)
        # The kind for the new entity
        kind = "Bookmark"
        # The name/ID for the new entity
        #name = "foo"
        # 重複チェック
        query = client.query(kind=kind)
        result = list(query.add_filter('url', '=', json["url"]).fetch())
        if result:
            return "Already registered"

        # The Cloud Datastore key for the new entity
        bookmark_key = client.key(kind)
        #bookmark_key = client.key(kind, name)
        # Prepares the new entity
        bookmark = datastore.Entity(key=bookmark_key)
        bookmark["url"] = json["url"]
        bookmark["title"] = json["title"]
        bookmark["remarks"] = json["remarks"]
        bookmark["importance"] = int(json["importance"])
        bookmark["updated_at"] = datetime.utcnow()
        bookmark["created_at"] = datetime.utcnow()
        logging.debug(bookmark)
        # Saves the entity
        client.put(bookmark)
        logging.debug('now leave post bookmarks')
        return bookmark
    else:   #GET method
        logging.debug('now in get bookmarks')
        sortItem = request.args.get('sortItem')
        sortAsc = request.args.get('sortAsc')
        logging.debug(sortItem)
        logging.debug(sortAsc)
        # The kind for the new entity
        kind = "Bookmark"
        query = client.query(kind=kind)
        #logging.debug(query)
        # ソート
        if sortItem == "1":
            logging.debug("sortItem == 1")
            if sortAsc == "1":
                query.order = ["created_at"]
            else:
                query.order = ["-created_at"]
        elif sortItem == "2":
            logging.debug("sortItem == 2")
            if sortAsc == "1":
                query.order = ["updated_at"]
            else:
                query.order = ["-updated_at"]
        elif sortItem == "3":
            logging.debug("sortItem == 3")
            if sortAsc == "1":
                query.order = ["url"]
            else:
                query.order = ["-url"]
        elif sortItem == "4":
            logging.debug("sortItem == 4")
            if sortAsc == "1":
                query.order = ["importance"]
            else:
                query.order = ["-importance"]
        else:
            logging.debug("sortItem != 1～4")
            query.order = ["created_at"]

        result = list(query.fetch())
        #logging.debug(result)

        if not result:
            logging.debug('now leave get bookmarks')
            return ""

        bookmarks = []
        for item in result:
            obj = dict(item)
            #logging.debug(obj)
            obj["id"] = item.key.id
            #obj["importance"] = int(item.importance)
            #logging.debug(obj)
            bookmarks.append(obj)

        logging.debug('now leave get bookmarks')
        return jsonify(bookmarks, sortItem, sortAsc)
        # logging.debug(jsonify(result))
        # return jsonify(result)

@bookmarks_bp.route('/show', methods=['GET'])
def show_bookmark():
    logging.debug('now in get bookmarks/show/<id>')
    targetid = request.args.get('id')
    logging.debug(targetid)
    key = client.key("Bookmark", int(targetid))
    result = client.get(key)
    logging.debug(result)
    if not result:
        logging.debug('now leave get bookmarks/show/<id>')
        return ""

    obj = dict(result)
    logging.debug(obj)
    obj["id"] = result.key.id
    logging.debug(obj)

    logging.debug('now leave get bookmarks/show/<id>')
    return jsonify(obj)


@bookmarks_bp.route('/update/<targetid>', methods=['PUT'])
def update_bookmark(targetid):
    logging.debug('now in put bookmarks/update/<id>')
    json = request.get_json()
    logging.debug(json)
    logging.debug(targetid)
    key = client.key("Bookmark", int(targetid))
    result = client.get(key)
    result["url"] = json["url"]
    result["title"] = json["title"]
    result["remarks"] = json["remarks"]
    result["importance"] = int(json["importance"])
    result["updated_at"] = datetime.utcnow()
    #result["created_at"] = datetime.utcnow()
    logging.debug(result)
    # Saves the entity
    client.put(result)
    logging.debug('now leave put bookmarks/update/<id>')

    logging.debug(targetid)
    key = client.key("Bookmark", int(targetid))
    result = client.get(key)
    logging.debug(result)
    if not result:
        logging.debug('now leave put bookmarks/update/<id>')
        return ""

    obj = dict(result)
    logging.debug(obj)
    obj["id"] = result.key.id
    logging.debug(obj)

    logging.debug('now leave put bookmarks/update/<id>')
    return jsonify(obj)


@bookmarks_bp.route('/delete/<targetid>', methods=['DELETE'])
def delete_bookmark(targetid):
    logging.debug('now in delete bookmarks/delete/<id>')
    logging.debug(targetid)
    key = client.key("Bookmark", int(targetid))
    result = client.get(key)
    logging.debug(result)
    # delete the entity
    client.delete(result)
    logging.debug('now leave delete bookmarks/delete/<id>')

    # The kind for the new entity
    kind = "Bookmark"
    query = client.query(kind=kind)
    logging.debug(query)
    result = list(query.fetch())
    logging.debug(result)
    if not result:
        logging.debug('now leave delete bookmarks/delete/<id>')
        return ""

    bookmarks = []
    for item in result:
        obj = dict(item)
        logging.debug(obj)
        obj["id"] = item.key.id
        logging.debug(obj)
        bookmarks.append(obj)

    logging.debug('now leave delete bookmarks')
    return jsonify(bookmarks)

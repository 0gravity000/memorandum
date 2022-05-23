from flask import Flask, jsonify, render_template, request, Blueprint
import logging
import json
from google.cloud import datastore
from datetime import date, datetime
from common import add_keyid_queryresult
from bookmark_tags import BookmarkTags
#from bookmark_tags import BookmarkTags, show_bookmark_tags, update_bookmark_tags
from tags import Tag

# Instantiates a client
client = datastore.Client()
# Blueprintオブジェクトを生成
bookmarks_bp = Blueprint('bookmarks', __name__, url_prefix='/api/bookmarks')

@bookmarks_bp.route('/', methods=['GET', 'POST'])
def bookmarks():
    bookmark = Bookmark()
    if request.method == 'POST':    #POST Method
        return bookmark.post_bookmark()
    else:   #GET method
        sortItem = request.args.get('sortItem')
        sortAsc = request.args.get('sortAsc')
        logging.debug(sortItem)
        logging.debug(sortAsc)
        bookmarks = bookmark.get_bookmarks(sortItem, sortAsc)
        # タグを取得
        tag = Tag()
        tags = tag.get_tags()
        # ブックマークタグを取得
        bookmarktags = BookmarkTags()
        bookmark_tags = bookmarktags.get_bookmark_tags()
        # logging.debug(bookmarks)
        # logging.debug(sortItem)
        # logging.debug(sortAsc)
        # logging.debug(tags)
        # logging.debug(bookmark_tags)
        return jsonify(bookmarks, sortItem, sortAsc, tags, bookmark_tags)
        #return jsonify(bookmarks)

@bookmarks_bp.route('/show', methods=['GET'])
def show_bookmark():
    bookmark = Bookmark()
    return bookmark.show_bookmark()

@bookmarks_bp.route('/update/<targetid>', methods=['PUT'])
def update_bookmark(targetid):
    bookmark = Bookmark()
    return bookmark.update_bookmark(targetid)

@bookmarks_bp.route('/delete/<targetid>', methods=['DELETE'])
def delete_bookmark(targetid):
    bookmark = Bookmark()
    return bookmark.delete_bookmark(targetid)

class Bookmark():
    def __init__(self):
        pass

    def get_bookmarks(self ,sortItem ,sortAsc):
        logging.debug('now in get bookmarks')
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

        bookmarks = add_keyid_queryresult(result)

        logging.debug('now leave get bookmarks')
        return bookmarks
        # return jsonify(bookmarks)
        # return jsonify(bookmarks, sortItem, sortAsc)

    def post_bookmark(self):
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
        logging.debug('★★★')
        client.put(bookmark)
        bookmarkid = bookmark.key.id
        logging.debug(bookmarkid)

        checkedTags = json["checkedTags"]
        addlist = []
        if checkedTags:
            for checkedtag in checkedTags:
                # 重複チェック
                query = client.query(kind="BookmarkTags")
                query.add_filter('bookmark_id', '=', int(bookmarkid))
                query.add_filter('tag_id', '=', checkedtag)
                result = list(query.fetch())
                if result:
                    continue
                # The Cloud Datastore key for the new entity
                bookmarktag_key = client.key("BookmarkTags")
                # Prepares the new entity
                bookmarktag = datastore.Entity(key=bookmarktag_key)
                bookmarktag["bookmark_id"] = bookmarkid
                bookmarktag["tag_id"] = checkedtag
                bookmarktag["updated_at"] = datetime.utcnow()
                bookmarktag["created_at"] = datetime.utcnow()
                logging.debug(bookmarktag)
                # Saves the entity
                client.put(bookmarktag)

        logging.debug('now leave post bookmarks')
        return bookmark

    def show_bookmark(self):
        logging.debug('now in get bookmarks/show/<id>')
        targetid = request.args.get('id')
        logging.debug(targetid)
        key = client.key("Bookmark", int(targetid))
        result = client.get(key)
        logging.debug(result)
        if not result:
            logging.debug('now leave get bookmarks/show/<id>')
            return ""

        bookmarks = dict(result)
        logging.debug(bookmarks)
        bookmarks["id"] = result.key.id
        logging.debug(bookmarks)
        # タグを取得
        query = client.query(kind='Tag')
        query.order = ["name"]
        result = list(query.fetch())
        tags = add_keyid_queryresult(result)
        logging.debug(tags)
        bookmarktags = BookmarkTags()
        bookmark_tags = bookmarktags.show_bookmark_tags(targetid)
        logging.debug(bookmark_tags)

        logging.debug('now leave get bookmarks/show/<id>')
        return jsonify(bookmarks, tags, bookmark_tags)

    def update_bookmark(self, targetid):
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

        #ブックマークを取得
        logging.debug(targetid)
        key = client.key("Bookmark", int(targetid))
        result = client.get(key)
        logging.debug(result)
        if not result:
            logging.debug('now leave put bookmarks/update/<id>')
            return ""

        bookmarks = dict(result)
        logging.debug(bookmarks)
        bookmarks["id"] = result.key.id
        logging.debug(bookmarks)

        #タグを取得
        query = client.query(kind='Tag')
        query.order = ["name"]
        result = list(query.fetch())
        #logging.debug(tags)
        tags = add_keyid_queryresult(result)
        #ブックマーク_タグを更新
        bookmarktags = BookmarkTags()
        bookmark_tags = bookmarktags.update_bookmark_tags(targetid, json["checkedTags"])

        logging.debug('now leave put bookmarks/update/<id>')
        return jsonify(bookmarks, tags, bookmark_tags)

    def delete_bookmark(self, targetid):
        logging.debug('now in delete bookmarks/delete/<id>')
        logging.debug(targetid)
        key = client.key("Bookmark", int(targetid))
        result = client.get(key)
        logging.debug(result)
        # delete the entity
        client.delete(result)
        logging.debug('now leave delete bookmarks/delete/<id>')

        #BookmarkTagsエンティティから該当ブックマークを削除
        bookmarktags = BookmarkTags()
        bookmarktags.delete_bookmarks(targetid)

        #削除後、残りのentityを返す
        # The kind for the new entity
        kind = "Bookmark"
        query = client.query(kind=kind)
        logging.debug(query)
        result = list(query.fetch())
        logging.debug(result)
        if not result:
            logging.debug('now leave delete bookmarks/delete/<id>')
            return ""

        bookmarks = add_keyid_queryresult(result)

        logging.debug('now leave delete bookmarks/delete/<id>')
        return jsonify(bookmarks)

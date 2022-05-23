from flask import Flask, jsonify, render_template, request, Blueprint
import logging
import json
from google.cloud import datastore
from datetime import date, datetime
from common import add_keyid_queryresult

# Instantiates a client
client = datastore.Client()

# Blueprintオブジェクトを生成
tags_bp = Blueprint('tags', __name__, url_prefix='/api/tags')

@tags_bp.route('/', methods=['GET', 'POST'])
def tags():
    tag = Tag()
    if request.method == 'POST':    #POST Method
        return tag.post_tag()
    else:   #GET method
        return jsonify(tag.get_tags())

@tags_bp.route('/show', methods=['GET'])
def show_tag():
    tag = Tag()
    return tag.show_tag()

@tags_bp.route('/update/<targetid>', methods=['PUT'])
def update_tag(targetid):
    tag = Tag()
    return tag.update_tag()

@tags_bp.route('/delete/<targetid>', methods=['DELETE'])
def delete_tag(targetid):
    tag = Tag()
    return tag.delete_tag()
class Tag():
    def __init__(self):
        pass

    def get_tags(self):
        logging.debug('now in get tags')
        # The kind for the new entity
        kind = "Tag"
        query = client.query(kind=kind)
        #logging.debug(query)
        # ソート
        query.order = ["name"]
        result = list(query.fetch())
        #logging.debug(result)

        if not result:
            logging.debug('now leave get tags')
            return ""

        tags = add_keyid_queryresult(result)
        '''
        tags = []
        for item in result:
            obj = dict(item)
            #logging.debug(obj)
            obj["id"] = item.key.id
            #logging.debug(obj)
            tags.append(obj)
        '''

        logging.debug('now leave get tags')
        return tags
        # return jsonify(tags)
    
    def post_tag(self):
        logging.debug('now in post tags')
        json = request.get_json()
        logging.debug(json)
        # The kind for the new entity
        kind = "Tag"
        # The name/ID for the new entity
        #name = "foo"
        # 重複チェック
        query = client.query(kind=kind)
        result = list(query.add_filter('name', '=', json["name"]).fetch())
        if result:
            return "Already registered"

        # The Cloud Datastore key for the new entity
        tag_key = client.key(kind)
        # Prepares the new entity
        tag = datastore.Entity(key=tag_key)
        tag["name"] = json["name"]
        tag["remarks"] = json["remarks"]
        tag["updated_at"] = datetime.utcnow()
        tag["created_at"] = datetime.utcnow()
        logging.debug(tag)
        # Saves the entity
        client.put(tag)
        logging.debug('now leave post tags')
        return tag

    def show_tag(self):
        logging.debug('now in get tags/show/<id>')
        targetid = request.args.get('id')
        logging.debug(targetid)
        key = client.key("Tag", int(targetid))
        result = client.get(key)
        logging.debug(result)
        if not result:
            logging.debug('now leave get tags/show/<id>')
            return ""

        obj = dict(result)
        logging.debug(obj)
        obj["id"] = result.key.id
        logging.debug(obj)

        logging.debug('now leave get tags/show/<id>')
        return jsonify(obj)

    def update_tag(self, targetid):
        logging.debug('now in put tags/update/<id>')
        json = request.get_json()
        logging.debug(json)
        logging.debug(targetid)
        key = client.key("Tag", int(targetid))
        result = client.get(key)
        result["name"] = json["name"]
        result["remarks"] = json["remarks"]
        result["updated_at"] = datetime.utcnow()
        #result["created_at"] = datetime.utcnow()
        logging.debug(result)
        # Saves the entity
        client.put(result)
        logging.debug('now leave put tags/update/<id>')

        logging.debug(targetid)
        key = client.key("Tag", int(targetid))
        result = client.get(key)
        logging.debug(result)
        if not result:
            logging.debug('now leave put tags/update/<id>')
            return ""

        obj = dict(result)
        logging.debug(obj)
        obj["id"] = result.key.id
        logging.debug(obj)

        logging.debug('now leave put tags/update/<id>')
        return jsonify(obj)

    def delete_tag(self, targetid):
        logging.debug('now in delete tags/delete/<id>')
        logging.debug(targetid)
        key = client.key("Tag", int(targetid))
        result = client.get(key)
        logging.debug(result)
        # delete the entity
        client.delete(result)
        logging.debug('now leave delete tags/delete/<id>')

        #BookmarkTagsエンティティから削除
        # The kind for the new entity
        kind = "BookmarkTags"
        query = client.query(kind=kind)
        query.add_filter('tag_id', '=', int(targetid))
        result = list(query.fetch())
        logging.debug(result)
        if result:
            for item in result:
                logging.debug(item)
                client.delete(item)

        #削除後、残りのentityを返す
        # The kind for the new entity
        kind = "Tag"
        query = client.query(kind=kind)
        logging.debug(query)
        result = list(query.fetch())
        logging.debug(result)
        if not result:
            logging.debug('now leave delete tags/delete/<id>')
            return ""

        tags = add_keyid_queryresult(result)
        '''
        tags = []
        for item in result:
            obj = dict(item)
            logging.debug(obj)
            obj["id"] = item.key.id
            logging.debug(obj)
            tags.append(obj)
        '''

        logging.debug('now leave delete tags/delete/<id>')
        return jsonify(tags)

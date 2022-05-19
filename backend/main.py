from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import json
from google.cloud import datastore
from datetime import date, datetime
#from model import User, Bookmark, Tag, BookmarkUser, BookmarkTag

# instantiate the app
app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
#app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# LEVEL を DEBUG に変更
logging.basicConfig(level=logging.DEBUG)

# Instantiates a client
client = datastore.Client()

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


@app.route('/api/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    if request.method == 'POST':
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
        bookmark["updated_at"] = datetime.utcnow()
        bookmark["created_at"] = datetime.utcnow()
        logging.debug(bookmark)
        # Saves the entity
        client.put(bookmark)
        logging.debug('now leave post bookmarks')
        return bookmark
    else:   #GET method
        logging.debug('now in get bookmarks')
        # The kind for the new entity
        kind = "Bookmark"
        query = client.query(kind=kind)
        logging.debug(query)
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
            #logging.debug(obj)
            bookmarks.append(obj)

        logging.debug('now leave get bookmarks')
        return jsonify(bookmarks)
        # logging.debug(jsonify(result))
        # return jsonify(result)


@app.route('/api/bookmarks/show', methods=['GET'])
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


@app.route('/api/bookmarks/update/<targetid>', methods=['PUT'])
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


@app.route('/api/bookmarks/delete/<targetid>', methods=['DELETE'])
def delete_bookmark(targetid):
    logging.debug('now in delete bookmarks/delete/<id>')
    logging.debug(targetid)
    key = client.key("Bookmark", int(targetid))
    result = client.get(key)
    logging.debug(result)
    # delete the entity
    client.delete(result)
    logging.debug('now leave delete bookmarks')

    # The kind for the new entity
    kind = "Bookmark"
    query = client.query(kind=kind)
    logging.debug(query)
    result = list(query.fetch())
    logging.debug(result)
    if not result:
        logging.debug('now leave delete bookmarks')
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

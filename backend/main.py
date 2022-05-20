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

# instantiate the app
app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
#app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(bookmarks_bp)

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

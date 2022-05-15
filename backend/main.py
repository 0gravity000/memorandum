from flask import Flask, jsonify, render_template
from flask_cors import CORS

# instantiate the app
app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
#app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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

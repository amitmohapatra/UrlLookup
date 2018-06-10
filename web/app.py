__author__ = 'Amit Mohapatra'

import hashlib
import sqlite3

from flask import g
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
DATABASE = '/db/test.db'

# get the db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# query the db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


#get request to check the url
@app.route('/urlinfo/1/<string:host_port>/')
@app.route('/urlinfo/1/<string:host_port>/<path:url_path>')
def lookup(host_port, url_path=None):
    url_path = request.full_path.replace('/urlinfo/1/', '')
    hash_val = hashlib.md5(url_path).hexdigest()
    create_table()
    insert_records()
    result = query_db('select * from lookup where hash = ?', [hash_val], one=True)

    if result:
        data = jsonify({'category': 'negetive',
                        'content': 'malware',
                        'assessment': 'very poor',
                        'status': 'found'})
    else:
        data = jsonify({'status': 'missing'})
    return make_response(data, 200)


def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS lookup(hash TEXT, url TEXT, UNIQUE(hash, url))''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS lookup_index ON lookup (hash)''')
    db.commit()
    cursor.close()


def insert_records():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM lookup''')
    rows = [('560975b9f71d4cce8f04039a3f71b4de', 'www.google.co.in/imghp?hl=en&tab=wi'),
            ('329df3d5aefae0d6f3e3fd06c0c06003', '127.0.0.1:8080/test?test=true')]
    cursor.executemany('insert into lookup values (?,?)', rows)
    db.commit()
    cursor.close()


@app.errorhandler(400)
def invaid_response(error):
    data = jsonify({'error': 'Invaid Request'})
    return make_response(data, 400)


@app.errorhandler(500)
def invaid_response_five(error):
    data = jsonify({'error': 'Internal error'})
    return make_response(data, 500)


if __name__ == "__main__":
    app.run()

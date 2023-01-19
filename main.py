from cProfile import run
from unicodedata import name
from flask import Flask , redirect , request ,make_response , render_template , url_for ,g ,config , flash , session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from hashids import Hashids
from datetime import datetime
import sqlite3
import os

current_timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app =  Flask(__name__)
app.config['SECRET_KEY'] = 'this is a really really really really long secret string'

hashids = Hashids(min_length=4 , salt=app.config['SECRET_KEY'])


@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url: 
            flash('You didn\'t enter the required field !! URL is required !')
            return redirect(url_for('index'))

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',(url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id) 
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url,clicks FROM urls WHERE id = (?)',(original_id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',(clicks+1,original_id))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL entered')
        return redirect(url_for('index')) 

@app.route('/stats')
def stats():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id,created,original_url,clicks FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    return render_template('stats.html',urls=urls,current_timestamp=current_timestamp)


if __name__ == '__main__':
    app.run(debug=True)
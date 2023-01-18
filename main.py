from cProfile import run
from unicodedata import name
from flask import Flask , redirect , request ,make_response , render_template , url_for ,g ,config , flash , session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from hashids import Hashids
import sqlite3
import os


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

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                                (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
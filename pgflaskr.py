# all the imports
import os
import sys

'DATABASE_URL' in os.environ or sys.exit('DATABASE_URL must be in the environment')

import urlparse
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

# configuration
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
  return psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )

# create database objects using migrations
# http://pseudofish.com/postgres-database-migrations-with-python.html
# foreman start db_init (once)
# foreman start migrate

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = connect_db()
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

def make_dicts(cur, row):
  return dict((cur.description[idx][0], value)
              for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
  db = get_db()
  cur = db.cursor()
  cur.execute(query, args)
  rv = []
  row = cur.fetchone()
  while row is not None:
    rv.append(make_dicts(cur, row))
    row = cur.fetchone()
  cur.close()
  return (rv[0] if rv else None) if one else rv

@app.route('/')
def show_entries():
  entries = query_db('select title, text from entries order by id desc')
  return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  db = get_db()
  cur = db.cursor()
  cur.execute('insert into entries (title, text) values (%s, %s)',
               [request.form['title'], request.form['text']])
  db.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_entries'))

if __name__ == '__main__':
  #try:
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 5000), app)
    print 'starting gevent server'
    http_server.serve_forever()
  #except:
  #  app.run()

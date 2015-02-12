# pgflaskr

This started with the flask tutorial at http://flask.pocoo.org/docs/0.10/tutorial/introduction/, then
* Migrated to PostgreSQL (using psycopg2 at http://initd.org/psycopg/docs/usage.html) instead of SQLite3
* Added database migration based on http://pseudofish.com/postgres-database-migrations-with-python.html
* Added ability to run as gevent server (requires Python 2.7.5 or later on Windows http://stackoverflow.com/questions/17556087/greenlet-in-win-7-dll-failed-the-specified-procedure-could-not-be-found)
* Added packaging to run on Heroku (https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* Configured gunicorn to use gevent workers (http://docs.gunicorn.org/en/develop/configure.html)

# Deploy

```bash
git clone https://github.com/talkingscott/pgflaskr.git
cd pgflaskr
heroku create
git push heroku master
heroku run db_init
heroku run migrate
heroku ps:scale web=1
heroku ps
heroku open
```

# License

The flask tutorial is © Copyright 2013, Armin Ronacher.

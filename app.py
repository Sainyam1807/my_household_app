from flask import Flask #,render_template(dont want this now)

from backend.models import db

# from sqlalchemy import event
# from sqlalchemy.engine import Engine
# import sqlite3

#setting up of app
app=None

def setup_app():
    app = Flask(__name__)  #flask object
    app.debug=True
    #pending is sqlite connection
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household_services.sqlite3"  #giving sqlite file name |  db(sqlalchemy) is connected to sqlite
    db.init_app(app) #flask app connected to db(SQLAlchemy)
    app.app_context().push() #direct access to other modules like backend folder
    print("household app is starting....")
    # app.secret_key = 'your_secret_key'   # to be checked

#calling the setup app function
setup_app()

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection, sqlite3.Connection):  # Apply only to SQLite connections
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA busy_timeout = 5000;")  # Wait up to 5 seconds for the lock to be released
#         cursor.close()

#accessing controllers.py in this
from backend.controllers import *

if __name__ == '__main__':
    app.run()
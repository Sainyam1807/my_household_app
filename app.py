from flask import Flask #,render_template(dont want this now)

from backend.models import db

#setting up of app
app=None

def setup_app():
    app = Flask(__name__)  #flask object
    app.debug=True
    #pending is sqlite connection
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household_services.sqlite3"  #giving sqlite file name |  db(sqlalchemy) is connected to sqlite
    db.init_app(app) #flask app connected to db(SQLAlchemy)
    app.app_context().push() #direct access to other modukes like backend folder
    print("household app is staring....")

#calling the setup app function
setup_app()

#accessing controllers.py in this
from backend.controllers import *

if __name__ == '__main__':
    app.run()
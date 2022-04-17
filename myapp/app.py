import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL

mysql = MySQL()


def create_app():
    app = Flask(__name__,template_folder='web',static_folder='web/static')
    # mysql connection details
    app.config['MYSQL_HOST'] = os.environ.get('SQL_HOST')
    app.config['MYSQL_USER'] = os.environ.get('USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('DB')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 
    
    cors = CORS(app, resources=r'/*')
    app.config.from_object('myapp.config')
    app.secret_key = os.environ.get('SECRET_KEY')
    
    mysql.init_app(app)
    register_blueprints(app)
    return app



def register_blueprints(app: Flask):
    from . import auth, errorhandlers
    #logins, forgot password and account activation
    app.register_blueprint(auth.routes.blueprint)
    #error handlers
    app.register_blueprint(errorhandlers.routes.blueprint)


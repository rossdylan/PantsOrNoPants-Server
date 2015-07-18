from flask import Flask
from flask_restful import Resource, Api
from ponp_server.database import db_session


app = Flask(__name__)
api = Api(app)


@app.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()

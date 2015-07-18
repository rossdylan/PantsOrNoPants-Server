from flask import Flask
from flask_restful import Resource, Api, reqparse
from ponp_server.database import db_session


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('api_key', type=str, help='API Key for this account')


@app.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()


class UserList(Resource):
    def post(self):
        """"
        Create a new user. NO API KEY
        """
        return {}, 200


class User(Resource):
    def get(self, uid):
        """
        Get the user given by the uid. API KEY
        """
        args = parser.parse_args()
        return {}, 200

    def put(self, uid):
        """
        Update an user. API KEY
        """
        args = parser.parse_args()
        return {}, 200


class Pants(Resource):
    def get(self):
        """
        Return the PCI Report for this user today. API KEY
        """
        args = parser.parse_args()
        return {}, 200


api.add_resource(Pants, '/api/v1/pants')
api.add_resource(User, '/api/v1/users/<uid>')
api.add_resource(UserList, '/api/v1/users')


if __name__ == '__main__':
    app.run(debug=True)

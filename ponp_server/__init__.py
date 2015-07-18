from flask import Flask
from flask_restful import Resource, Api, reqparse
from ponp_server.database import db_session
from ponp_server.models.users import User as UserModel
from ponp_server.parsers import (lang_parser,
                                 gender_parser,
                                 inclination_parser,
                                 apikey_parser)


app = Flask(__name__)
api = Api(app)


ak_parser = reqparse.RequestParser()
ak_parser.add_argument('apikey',
                       type=apikey_parser,
                       help='API Key for this account',
                       required=True)


@app.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()


class Auth(Resource):
    def post(self):
        """
        Authenticate as a user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('pass', type=str, required=True)

        query = db_session.query(UserModel).filter(
            UserModel.username == args['name'])
        if query.count() > 0:
            user = query.one()
            if user.password == args['pass']:
                user.apikey = generate_apikey(user.username)
                db_session.update(user)
                db_session.commit()
                return {'apikey': user.apikey}, 200
        return {"message": {"pass": "User or Password is Incorrect",
                        "user": "User or Password is Incorrect", }}, 400


class UserList(Resource):
    def post(self):
        """"
        Create a new user. NO API KEY
        """
        parser = reqparse.RequestParser()
        parser.add_argument('lang', type=lang_parser)
        parser.add_argument('user', type=str, required=True)

        parser.add_argument('home_lat', type=float, required=True)
        parser.add_argument('home_lng', type=float, required=True)

        parser.add_argument('password', type=str, required=True)
        parser.add_argument('height', type=float, required=True)
        parser.add_argument('weight', type=float, required=True)
        parser.add_argument('gender', type=gender_parser, required=True)
        parser.add_argument('inclination', type=inclination_parser, required=True)

        args = parser.parse_args(strict=True)
        user = UserModel.new_user(args['user'],
                                  args['lang'],
                                  args['home_lat'],
                                  args['home_lng'],
                                  args['password'],
                                  args['height'],
                                  args['weight'],
                                  args['gender'],
                                  args['inclination'])
        return user.to_dict(), 200


class User(Resource):
    def get(self, uid):
        """
        Get the user given by the uid. API KEY
        """

        parser = ak_parser.copy()
        args = parser.parse_args(strict=True)
        return {}, 200

    def put(self, uid):
        """
        Update an user. API KEY
        """

        parser = ak_parser.copy()
        args = parser.parse_args(strict=True)
        return {}, 200


class Pants(Resource):
    def get(self):
        """
        Return the PCI Report for this user today. API KEY
        """

        parser = ak_parser.copy()
        args = parser.parse_args(strict=True)
        return {}, 200


api.add_resource(Auth, '/api/v1/auth')
api.add_resource(Pants, '/api/v1/pants')
api.add_resource(User, '/api/v1/users/<uid>')
api.add_resource(UserList, '/api/v1/users')


if __name__ == '__main__':
    app.run(debug=True)

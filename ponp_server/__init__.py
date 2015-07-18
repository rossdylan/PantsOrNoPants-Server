from flask import Flask
from flask_restful import Resource, Api, reqparse
from ponp_server.database import db_session
from ponp_server.models.users import User as UserModel
from ponp_server.utils import generate_apikey
from ponp_server.weather import get_weather
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
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args(strict=True)

        query = db_session.query(UserModel).filter(
            UserModel.username == args['username'])
        if query.count() > 0:
            user = query.one()
            if user.password == args['password']:
                user.apikey = generate_apikey(user.username)
                db_session.merge(user)
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
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args(strict=True)
        print(args)
        user = UserModel.new_user(args['username'], args['password'])
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
        parser.add_argument('lang', type=lang_parser)
        parser.add_argument('height', type=float)
        parser.add_argument('weight', type=float)
        parser.add_argument('gender', type=gender_parser)
        parser.add_argument('inclination', type=inclination_parser)
        args = parser.parse_args(strict=True)
        valid_fields = frozenset(['lang', 'height', 'weight', 'gender', 'inclination'])
        print args
        user_query = db_session.query(UserModel).filter(UserModel.apikey == args['apikey'])
        user = user_query.one()

        for key, value in args.iteritems():
            if key in valid_fields:
                setattr(user, key, value)
        db_session.merge(user)
        db_session.commit()
        return user.to_dict(), 200


class Pants(Resource):
    def get(self):
        """
        Return the PCI Report for this user today. API KEY
        """

        parser = ak_parser.copy()
        parser.add_argument('lat', type=float, required=True)
        parser.add_argument('lng', type=float, required=True)
        args = parser.parse_args(strict=True)
        wdata = get_weather(args['lat'], args['lng'])
        return wdata, 200


api.add_resource(Auth, '/api/v1/auth')
api.add_resource(Pants, '/api/v1/pants')
api.add_resource(User, '/api/v1/users/<uid>')
api.add_resource(UserList, '/api/v1/users')


if __name__ == '__main__':
    app.run(debug=True)

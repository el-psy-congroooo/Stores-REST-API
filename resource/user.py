import sqlite3
from flask_restful import Resource, reqparse
from model.user import UserModel


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User registered successfully"}, 201

from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
)
from model.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True,
                          help="This field cannot be left blank.")
_user_parser.add_argument('password', type=str, required=True,
                          help="This field cannot be left blank.")


class UserRegistration(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User registered successfully."}, 201


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        else:
            return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
        else:
            return {"message": "User not found."}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Invalid credentials.'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT id"
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}

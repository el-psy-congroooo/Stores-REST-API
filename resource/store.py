from flask_restful import Resource
from flask_jwt import jwt_required
from model.store import StoreModel


class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'error': 'store already exists'}, 400
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}
        return {'message': 'store not found'}, 404

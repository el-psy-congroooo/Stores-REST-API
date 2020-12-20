from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.item import ItemModel


class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field can not be left empty.')
    parser.add_argument('store_id', type=int, required=True,
                        help='Every item must have a store id.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'error': 'item already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted'}
        return {'message': 'item not found'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

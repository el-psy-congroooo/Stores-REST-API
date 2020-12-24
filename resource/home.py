from flask_restful import Resource


class HomePage(Resource):

    def get(self):
        return {
            'message': "This is a REST API to store data of 'Stores' and 'Items'. It has following endpoints: -",
            '/stores': 'To get data of all the sotres.',
            '/items': 'To get data of all the items.',
            '/store/<string:name>': 'To get the data of a specific store.',
            '/item/<string:name>': 'To get the data of a specific item.',
            '/register': 'To SignUp for the API.',
            '/user<int:user_id>': 'To get the username and user id of an user using his user id.',
            '/login': 'To login into the API.',
            '/logout': 'To logout from the API.',
            '/refresh': 'To refresh the JWT access token.',
            'Note: -': "You have to enter the name of 'Store' or 'Item' in place of '<string:name>' and user id in place of '<int:user_id>'.",
            'Made By: -':'Nishant Awasthi'
        }
from flask_app.config.mysqlconnection import connectToMySQL

class Collection:
    DATABASE = 'mtg_collections'

    def __init__(self, data):
        self.user_id = data['user_id']
        self.card_id = data['card_id']
        self.quantity = data['quantity']
        self.style = data['style']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO collections (user_id, card_id, quantity, style) ' \
            'VALUES (%(user_id)s, %(card_id)s, %(quantity)s, %(style)s);'
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_by_ids(cls, card_id, user_id):
        data = {
            'card_id': card_id,
            'user_id': user_id
        }
        query = 'SELECT * FROM collections WHERE user_id = %(user_id)s AND ' \
            'card_id = %(card_id)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        if result:
            return cls(result[0])

        return False
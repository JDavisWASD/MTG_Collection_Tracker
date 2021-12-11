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
    def update(cls, card_id, style, quantity):
        data = {
            'quantity': quantity,
            'card_id': card_id,
            'style': style
        }
        query = 'UPDATE collections SET quantity = %(quantity)s WHERE card_id = %(card_id)s AND style = %(style)s;'
        connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, card_id, style):
        data = {
            'card_id': card_id,
            'style': style
        }
        query = 'DELETE FROM collections WHERE card_id = %(card_id)s AND style = %(style)s;'
        connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_all_cards(cls, user_id):
        data = {'user_id': user_id}
        query = 'SELECT * FROM collections LEFT JOIN users ON ' \
            'user_id = users.id JOIN cards on card_id = cards.id WHERE ' \
            'user_id = %(user_id)s;'
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_num_unique(cls, user_id):
        data = {'user_id': user_id}
        query = 'SELECT COUNT(*) FROM collections LEFT JOIN users ON ' \
            'user_id = users.id JOIN cards on card_id = cards.id WHERE ' \
            'user_id = %(user_id)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        return result[0]['COUNT(*)']

    @classmethod
    def get_num_total(cls, user_id):
        data = {'user_id': user_id}
        query = 'SELECT SUM(quantity) FROM collections LEFT JOIN users ON ' \
            'user_id = users.id JOIN cards on card_id = cards.id WHERE ' \
            'user_id = %(user_id)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        return result[0]['SUM(quantity)']

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
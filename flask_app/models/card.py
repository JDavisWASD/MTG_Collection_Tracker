import requests

from flask_app.config.mysqlconnection import connectToMySQL

class Card:
    DATABASE = 'mtg_collections'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.set_code = data['set_code']
        self.type = data['type']
        self.cost = data['cost']
        self.usd = data['usd']
        self.usd_foil = data['usd_foil']
        self.usd_etched = data['usd_etched']
        self.eur = data['eur']
        self.eur_foil = data['eur_foil']
        self.tix = data['tix']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO cards (name, set_code, type, cost, usd, ' \
            'usd_foil, usd_etched, eur, eur_foil, tix, created_at, ' \
            'updated_at) VALUES (%(name)s, %(set_code)s, %(type)s, %(cost)s, ' \
            '%(usd)s, %(usd_foil)s, %(usd_etched)s, %(eur)s, %(eur_foil)s, ' \
            '%(tix)s, NOW(), NOW());'
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE cards SET type = %(type)s, usd = %(usd)s, ' \
            'usd_foil = %(usd_foil)s, usd_etched = %(usd_etched)s, ' \
            'eur = %(eur)s, eur_foil = %(eur_foil)s, tix = %(tix)s, ' \
            'updated_at = NOW() WHERE id = %(card_id)s;'
        connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_by_name_and_set(cls, name, set_code):
        data = {
            'name': name,
            'set_code': set_code
        }
        query = 'SELECT * FROM cards WHERE name = %(name)s AND ' \
            'set_code = %(set_code)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        if result:
            return cls(result[0])

        return False

    @staticmethod
    def search_api(name, set_code):
        result = requests.get(f"https://api.scryfall.com/cards/named?exact={name}&set={set_code}")
        result = result.json()

        if result['object'] == 'error':
            return False

        data = {
            'image': result['image_uris']['normal'],
            'name': result['name'],
            'set_code': result['set'],
            'type': result['type_line'],
            'cost': result['mana_cost'],
            'description': result['oracle_text'],
            'usd': result['prices']['usd'],
            'usd_foil': result['prices']['usd_foil'],
            'usd_etched': result['prices']['usd_etched'],
            'eur': result['prices']['eur'],
            'eur_foil': result['prices']['eur'],
            'tix': result['prices']['tix']
        }

        if 'power' in result:
            data['power'] = result['power']
        if 'toughness' in result:
            data['toughness'] = result['toughness']

        return data
import re

from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DATABASE = 'mtg_collections'

    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_username(cls, username):
        data = {'username': username}
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        if result:
            return cls(result[0])

        return False

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (username, email, password, created_at, ' \
            'updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(),'\
            ' NOW());'
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @staticmethod
    def validate_new_user(form):
        is_valid = True

        if form['username'] == '':
            flash('A username is required.')
            is_valid = False
        if len(form['username']) < 3 or len(form['username']) > 45:
            flash('Usernames must be between 3 and 45 characters.')
            is_valid = False
        if User.get_by_username(form['username']):
            flash('An account with that username already exists.')
            is_valid = False

        if form['email'] == '':
            flash('An email is required.')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Invalid email address.')
            is_valid = False
        
        if form['password'] == '':
            flash('A password is required')
            is_valid = False
        if len(form['password']) < 8:
            flash('Passwords must be at least 8 characters')
            is_valid = False
        if form['confirm_password'] == '':
            flash('Please confirm your password.')
            is_valid = False
        if form['password'] != form['confirm_password']:
            flash('Passwords don\'t match.')
            is_valid = False

        return is_valid
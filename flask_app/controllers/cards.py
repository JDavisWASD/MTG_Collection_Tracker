import time

from datetime import datetime, timedelta
from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.card import Card
from flask_app.models.collection import Collection

@app.route('/card')
def displayCard():
    return render_template('displayCard.html', cardInfo = session['lastSearch'])

@app.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('collection.html')

@app.route('/search', methods = ['POST'])
def search():
    session['lastSearch'] = Card.search_api(request.form['name'], request.form['set_code'])
    if session['lastSearch'] == False:
        if request.form['set_code'] == '':
            flash(f"{request.form['name'].title()} was not found.")
            return redirect('/')
        
        flash(f"{request.form['name'].title()} from {request.form['set_code'].upper()} was not found.")
        return redirect('/')

    return redirect('/card')

@app.route('/add_card', methods = ['POST'])
def add_card():
    card_in_database = Card.get_by_name_and_set(request.form['name'], request.form['set_code'])
    card_id = 0

    #Add card to database
    if not card_in_database:
        data = Card.search_api(request.form['name'], request.form['set_code'])
        if not data:
            if request.form['set_code'] == '':
                flash(f"{request.form['name'].title()} was not found.")
                return redirect('/collection')
        
            flash(f"{request.form['name'].title()} from {request.form['set_code'].upper()} was not found.")
            return redirect('/collection')
        card_id = Card.save(data)

    #Update stale data
    elif datetime.now() - card_in_database.updated_at >= timedelta(hours = 24):
        data = Card.search_api(card_in_database.name, card_in_database.set_code)
        data['card_id'] = card_in_database.id
        card_id = card_in_database.id
        Card.update(data)

    else:
        card_id = card_in_database.id

    card_in_collection = Collection.get_by_ids(card_id, session['user_id'])

    #Add card to user's collection
    if not card_in_collection or request.form['style'] != str(card_in_collection.style):
        data = {
            'user_id': session['user_id'],
            'card_id': card_id,
            'quantity': request.form['quantity'],
            'style': request.form['style']
        }
        Collection.save(data)
    else:
        flash(f"You already have a that style of {request.form['name'].title()} in your collection.")
        return redirect('/collection')

    return redirect('/collection')
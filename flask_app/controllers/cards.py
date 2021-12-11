from datetime import datetime, timedelta
from time import sleep
from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.card import Card
from flask_app.models.collection import Collection
from flask_app.models.user import User

@app.route('/card')
def displayCard():
    logged_in = False
    if 'user_id' in session:
        logged_in = True
    return render_template('displayCard.html', cardInfo = session['lastSearch'], logged_in = logged_in)

@app.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect('/')

    out_of_date = False
    collection = Collection.get_all_cards(session['user_id'])

    for card in collection:
        if datetime.now() - card['cards.updated_at'] >= timedelta(hours = 24):
            out_of_date = True
            data = Card.search_api(card['name'], card['set_code'])
            data['card_id'] = card['card_id']
            Card.update(data)

            #Scryfall API asks for a 100 milliseconds of delay between requests
            sleep(0.1)

    if out_of_date:
        collection = Collection.get_all_cards(session['user_id'])

    return render_template('collection.html', collection = collection, \
        collection_length = len(collection), \
        total = Collection.get_num_total(session['user_id']), \
        unique = Collection.get_num_unique(session['user_id']), \
        username = User.get_by_id(session['user_id']).username)

@app.route('/display/<set_code>/<name>')
def display_from_collection(name, set_code):
    session['lastSearch'] = Card.search_api(name, set_code)
    return redirect('/card')

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
        flash(f"You already have that style of {request.form['name'].title()} in your collection.")
        return redirect('/collection')

    return redirect('/collection')

@app.route('/update', methods = ['POST'])
def update():
    collection = Collection.get_all_cards(session['user_id'])
    for i in range(len(collection)):
        if request.form[f"{i}_quantity"] == "0":
            Collection.delete(collection[i]['card_id'], collection[i]['style'])
        elif request.form[f"{i}_quantity"] != collection[i]['quantity']:
            Collection.update(collection[i]['card_id'], collection[i]['style'], request.form[f"{i}_quantity"])

    return redirect('/collection')
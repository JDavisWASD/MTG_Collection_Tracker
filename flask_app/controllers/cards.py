import requests
import time

from datetime import datetime, timedelta
from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.card import Card

@app.route('/card')
def displayCard():
    return render_template('displayCard.html', cardInfo = session['lastSearch'])

@app.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect('/')

    session['error_redirect'] = '/collection'
    return render_template('collection.html')

@app.route('/search', methods = ['POST'])
def search():
    session['lastSearch'] = search_api(request.form['name'], request.form['set_code'])
    return redirect('/card')

@app.route('/add_card', methods = ['POST'])
def add_card():
    existing_card = Card.get_by_name_and_set(request.form['name'], request.form['set_code'])
    if not existing_card:
        card_id = Card.save(search_api(request.form['name'], request.form['set_code']))
    elif datetime.now() - existing_card.updated_at >= timedelta(hours = 24):
        data = search_api(existing_card.name, existing_card.set_code)
        data['card_id'] = existing_card.id
        Card.update(data)

    if True:
        pass

    return redirect('/collection')

def search_api(name, set_code):
    result = requests.get(f"https://api.scryfall.com/cards/named?exact={name}&set={set_code}")
    result = result.json()

    if result['object'] == 'error':
#        flash(f"{name.title()} from {set_code.upper()} was not found.")
        flash('No card found')
        return redirect('/collection')

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
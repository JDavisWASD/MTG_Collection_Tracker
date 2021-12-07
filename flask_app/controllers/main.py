import requests

from flask import flash, redirect, render_template, request, session
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card')
def displayCard():
    return render_template('displayCard.html', cardInfo = session['lastSearch'])

@app.route('/search', methods = ['POST'])
def search():
    result = requests.get(f"https://api.scryfall.com/cards/named?exact={request.form['name']}&set={request.form['set']}")
    result = result.json()
    
    print(result['oracle_text'])

    data = {
        'image': result['image_uris']['normal'],
        'name': result['name'],
        'cost': result['mana_cost'],
        'type': result['type_line'],
        'description': result['oracle_text'],
        'prices' : {
            'usd': result['prices']['usd'],
            'usd_foil': result['prices']['usd_foil'],
            'usd_etched': result['prices']['usd_etched'],
            'eur': result['prices']['eur'],
            'eur_foil': result['prices']['eur'],
            'tix': result['prices']['tix']
        }
    }

    if 'power' in result:
        data['power'] = result['power']
    if 'toughness' in result:
        data['toughness'] = result['toughness']
    
    session['lastSearch'] = data
    return redirect('/card')
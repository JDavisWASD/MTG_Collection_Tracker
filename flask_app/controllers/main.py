import requests

from flask import flash, redirect, render_template, request, session
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card')
def displayCard():
    data = {
        'image': session['lastSearch']['image_uris']['normal'],
        'name': session['lastSearch']['name'],
        'cost': session['lastSearch']['mana_cost'],
        'type': session['lastSearch']['type_line'],
        'description': session['lastSearch']['oracle_text']
    }

    if 'power' in session['lastSearch']:
        data['power'] = session['lastSearch']['power']
    if 'toughness' in session['lastSearch']:
        data['toughness'] = session['lastSearch']['toughness']
        
    return render_template('displayCard.html', cardInfo = data)

@app.route('/search', methods = ['POST'])
def search():
    result = requests.get(f"https://api.scryfall.com/cards/named?exact={request.form['query']}")
    session['lastSearch'] = result.json()
    return redirect('/card')
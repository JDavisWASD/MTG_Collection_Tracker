import requests

from flask import flash, redirect, render_template, request, session
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card')
def displayCard():
    return render_template('displayCard.html', searchResult = session['lastSearch'])

@app.route('/search', methods = ['POST'])
def search():
    result = requests.get(f"https://api.scryfall.com/cards/named?exact={request.form['query']}")
    session['lastSearch'] = result.json()
#    print(session['lastSearch']['object'])
#    return redirect('/card')
    return redirect('/')
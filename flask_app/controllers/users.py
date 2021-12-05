import requests

from flask import flash, redirect, render_template, request
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    result = requests.get(f"https://api.scryfall.com/cards/named?exact={request.form['query']}")
    print(result.text)
    return redirect('/')
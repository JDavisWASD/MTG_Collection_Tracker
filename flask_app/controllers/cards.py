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
    existing_card = Card.get_by_name_and_set(request.form['name'], request.form['set_code'])
    if not existing_card:
        data = Card.search_api(request.form['name'], request.form['set_code'])
        if not data:
            if request.form['set_code'] == '':
                flash(f"{request.form['name'].title()} was not found.")
                return redirect('/collection')
        
            flash(f"{request.form['name'].title()} from {request.form['set_code'].upper()} was not found.")
            return redirect('/collection')

        card_id = Card.save(data)
    elif datetime.now() - existing_card.updated_at >= timedelta(hours = 24):
        data = Card.search_api(existing_card.name, existing_card.set_code)
        data['card_id'] = existing_card.id
        Card.update(data)

    if True:
        pass

    return redirect('/collection')
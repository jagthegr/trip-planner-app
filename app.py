#!/usr/bin/env python3
#make a flask hello world app
from flask import Flask, render_template, request, session, redirect, url_for
import os

from api.fetch_data import fetch_tripadvisor_data
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
@app.route('/')
def index():
    city = session.get('city', 'Tacoma')
    state = session.get('state', 'WA')

    if request.method == 'GET':
        if request.args.get('city'):
            city = request.args.get('city')
            session['city'] = city
        if request.args.get('state'):
            state = request.args.get('state')
            session['state'] = state
        # Category is no longer taken from request args directly,
        # as we will fetch all three categories.

    restaurants_data = fetch_tripadvisor_data(city, state, 'restaurants', use_cache_only=True)
    hotels_data = fetch_tripadvisor_data(city, state, 'hotels', use_cache_only=True)
    attractions_data = fetch_tripadvisor_data(city, state, 'attractions', use_cache_only=True)

    return render_template('index.html',
                           city=city,
                           state=state,
                           restaurants_data=restaurants_data,
                           hotels_data=hotels_data,
                           attractions_data=attractions_data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

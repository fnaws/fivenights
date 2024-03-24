from flask import Flask, render_template, request, jsonify
from market import Market
import symbolator
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
import numpy as np
app = Flask(__name__)

m = Market()


@app.route('/')
def index():
    global m

    big_data = []
    first_day = None
    # Get the data from the API

    symbs = symbolator.get_random()
    month = symbolator.random_date()
    print(symbs)
    for symb in symbs:
        try:
            data = m.load_data(
                function='TIME_SERIES_INTRADAY',
                symbol=symb,
                interval='1min',
                month=month,
                outputsize='full',
                extended_hours='false'
            )
            first_day, transformed_data = m.day_data(month_data=data)
        except:
            first_day, transformed_data, new_symb = m.exception_handler()
            first_day += "-01"
            symb = new_symb

        big_data.append([symb, transformed_data])

    # for preloaded data (failsafe)
    # raw_data = m.load_data(
    #     function='TIME_SERIES_INTRADAY',
    #     symbol='TSLA',  # Make this random
    #     interval='1min',
    #     month='2023-09',  # Make this random
    #     outputsize='full',
    #     extended_hours='false'
    # )
    # data = m.day_data(raw_data)  # Assume this returns a list of 5 elements, each being a day's data

    shares = 0
    wallet = 10000.00
    net_gain = 0.00
    
    # Convert YYYY-MM-DD to string
    # Example: 2023-09-01 -> September 1, 2023
    try:
        first_day = pd.to_datetime(first_day).strftime('%B %d, %Y')
    except:
        first_day = "\"could not fetch\""
    

    return render_template('index3.html', big_data=big_data, wallet=wallet, shares=shares, net_gain=net_gain, first_day=first_day)

@app.route('/buy', methods=['POST'])
def buy():
    # Assume these variables are updated somehow here
    wallet = request.form['wallet_amount']
    shares = request.form['shares']
    net_gain = request.form['net_gain']
    quantity = request.form['quantity']
    curr_price = request.form['curr_price']

    print(shares)
    wallet = float(wallet)
    shares = float(shares)
    net_gain = float(net_gain)
    try:
        quantity = float(quantity)
    except:
        return jsonify({"error": "That's not a number"}), 400
    #Verify quantity is a positive number
    if quantity <= 0:
        return jsonify({"error": "Quantity must be a non-zero positive number"}), 400
    curr_price = float(curr_price)
    wallet = wallet - (quantity * curr_price)
    shares = shares + quantity
    #wallet is always initially 10000
    net_gain = (wallet + (shares * curr_price) - 10000)/100

    #Float formatting
    wallet = round(wallet, 2)
    shares = round(shares, 2)
    net_gain = round(net_gain, 2)

    print(wallet)

    if wallet < 0:
        return jsonify({"error": "Insufficient funds in wallet"}), 400 

    # Or return them in a JSON request
    return jsonify(wallet=wallet, shares=shares, net_gain=net_gain)

@app.route('/sell', methods=['POST'])
def sell():
    # Assume these variables are updated somehow here
    wallet = request.form['wallet_amount']
    shares = request.form['shares']
    net_gain = request.form['net_gain']
    quantity = request.form['quantity']
    curr_price = request.form['curr_price']

    wallet = float(wallet)
    shares = float(shares)
    net_gain = float(net_gain)
    try:
        quantity = float(quantity)
    except:
        return jsonify({"error": "That's not a number"}), 400
    #Verify quantity is a positive number
    if quantity <= 0:
        return jsonify({"error": "Quantity must be a non-zero positive number"}), 400
    curr_price = float(curr_price)

    wallet = wallet + (quantity * curr_price)
    shares = shares - quantity
    net_gain = (wallet + (shares * curr_price) - 10000)/100

    #Float formatting
    wallet = round(wallet, 2)
    shares = round(shares, 2)
    net_gain = round(net_gain, 2)


    if shares < 0:
        return jsonify({"error": "Not enough shares"}), 400
 

    # Or return them in a JSON request
    return jsonify(wallet=wallet, shares=shares, net_gain=net_gain)
            
if __name__ == '__main__':
    app.run(debug=True)

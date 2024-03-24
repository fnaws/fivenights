from flask import Flask, render_template, request, jsonify
from market import Market
import simulator
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
    # Get the data from the API

    symbs = simulator.get_random()
    month = simulator.random_date()
    print(symbs)
    for symb in symbs:
        print(symb)
        data = m.load_data(
            function='TIME_SERIES_INTRADAY',
            symbol=symb,
            interval='1min',
            month=month,
            outputsize='full',
            extended_hours='false'
        )
        transformed_data = m.day_data(month_data=data)
        # Transform the data to plot, x is the time, y is average of high and low
        plotting_data = []
        for index, row in data.iterrows():
            plotting_data.append({
                'x': index,
                'y': np.mean([row['2. high'], row['3. low']])
            })
        x_data = [entry['x'] for entry in plotting_data]
        y_data = [entry['y'] for entry in plotting_data]

        big_data.append((symb, y_data))

    raw_data = m.load_data(
        function='TIME_SERIES_INTRADAY',
        symbol='TSLA',  # Make this random
        interval='1min',
        month='2023-09',  # Make this random
        outputsize='full',
        extended_hours='false'
    )
    data = m.day_data(raw_data)  # Assume this returns a list of 5 elements, each being a day's data

    # Initialize plotting data for 5 days
    plotting_data = {'x': [], 'y': []}
    for day_data in data:  # Assuming day_data is a list of open prices for the day
        day_x_data = range(len(day_data))  # Generate a range object for x-axis (minutes)
        day_y_data = day_data  # Y-axis data
        
        # Append day data to plotting data
        plotting_data['x'].append(day_x_data)
        plotting_data['y'].append(day_y_data)

    # graphJSON = json.dumps(plotting_data, cls=plotly.utils.PlotlyJSONEncoder)
    shares = 0
    wallet = 10000.00
    net_gain = 0.00

    return render_template('index.html', data=data, wallet=wallet, shares=shares, net_gain=net_gain)

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
    quantity = float(quantity)
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
    quantity = float(quantity)
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

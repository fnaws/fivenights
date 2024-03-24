from flask import Flask, render_template
from market import Market
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
    # Get the data from the API
    data = m.load_data(
        function='TIME_SERIES_INTRADAY',
        symbol='TSLA',
        interval='1min',
        month='2023-09',
        outputsize='full',
        extended_hours='false'
    )
    # transformed_data = m.day_data(month_data=data)
    # print(transformed_data)
    plotting_data = []
    # Transform the data to plot, x is the time, y is average of high and low
    for index, row in data.iterrows():
        plotting_data.append({
            'x': index,
            'y': np.mean([row['2. high'], row['3. low']])
        })
    x_data = [entry['x'] for entry in plotting_data]
    y_data = [entry['y'] for entry in plotting_data]

    # for day in transformed_data:


    # Create a Plotly line chart
    trace = go.Scatter(
        x=x_data, 
        y=y_data, 
        mode='lines+markers', 
        line=dict(width=6, color='blue'),  # Increased line thickness to 6
        marker=dict(size=10)
    )
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False)
    )
    data = [trace]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    layoutJSON = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON, layoutJSON=layoutJSON, x_data=x_data, y_data=y_data)
            
if __name__ == '__main__':
    app.run(debug=True)

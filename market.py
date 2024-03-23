import threading
import requests
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backend_bases import Event
 
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class Market:
    def on_focus_out(self, event: Event):
        global focus_timer
        if focus_timer is not None:
            focus_timer.cancel()  # cancel the old timer if it exists
        focus_timer = threading.Timer(15 * 60, plt.close)  # reset the timer
        focus_timer.start()

    def load_data(self, function, symbol, interval, adjusted=True, extended_hours=False, month=None, outputsize='compact', datatype='json'):
        # See if data is available in CSV   
        try:
            data = pd.read_csv(f'data/stocks/{symbol}/{month}.csv')
            return data
        except:
            pass

        __api_key = os.environ.get('VANTAGE_API_KEY') # Load the API key
        if __api_key is None:
            raise ValueError("Missing API key. Ensure the VANTAGE_API_KEY environment variable is set.")
        
        base_url = 'https://www.alphavantage.co/query?'

        # Constructing the query parameters based on the arguments provided
        params = {
            'function': function,
            'symbol': symbol,
            'interval': interval,
            'adjusted': str(adjusted).lower(),
            'extended_hours': str(extended_hours).lower(),
            'outputsize': outputsize,
            'datatype': datatype,
            'apikey':__api_key
        }

        # If the month parameter is provided, add it to the params dictionary
        if month:
            params['month'] = month

        # Constructing the full URL by concatenating the base_url with the query parameters
        url = base_url + '&'.join(f'{k}={v}' for k, v in params.items())

        # Making the API request
        r = requests.get(url)
        
        # Handling the response based on the datatype requested
        if datatype == 'json':
            data = r.json()
        # elif datatype == 'csv':
        #     data = pd.read_csv(url)  # Directly read the CSV into a DataFrame
        else:
            raise ValueError(f"Unsupported datatype: {datatype}")

        time_series_data = data[f'Time Series ({interval})']
        
        # Converting the time series data to a pandas DataFrame
        df = pd.DataFrame(time_series_data).T  # Transposing the DataFrame for better organization

        # Converting the index to datetime for better plotting
        df.index = pd.to_datetime(df.index)

        # Converting the data in the DataFrame to numeric for plotting
        df = df.apply(pd.to_numeric, errors='coerce')

        #Save data to CSV
        try:
            os.makedirs(f'data/stocks/{symbol}')
        except:
            pass
        try:
            df.to_csv(f'data/stocks/{symbol}/{month}.csv')
        except:
            pass
            #print("Directories already exist or could not be created")

        return df  

    def _view(self, data, display='day'):
        # Ensure data is a pandas DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data should be a pandas DataFrame")

        # Convert the index to datetime for better plotting
        data.index = pd.to_datetime(data.index)

        # Create a figure and axis
        fig, ax1 = plt.subplots()

        # Plot the closing prices
        color = 'tab:red'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Close Price', color=color)
        ax1.plot(data.index, data['4. close'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Create a second y-axis to plot the volume on the same plot
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Volume', color=color)
        ax2.plot(data.index, data['5. volume'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Format the x-axis to display times in 12-hour format
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))

        # Determine the title based on the display argument
        if display == 'day':
            title_date = data.index[0].strftime('%Y-%m-%d')
        elif display == 'month':
            title_date = data.index[0].strftime('%Y-%m')
            # Display the year separately from the month and day
            plt.annotate(data.index[0].strftime('%Y'), xy=(1, 1), xycoords='axes fraction', fontsize=12, ha='right')
        else:
            raise ValueError(f"Unsupported display value: {display}")

        # Set the title
        plt.title(f'{title_date} IBM Intraday ({data.index[-1].strftime("%I:%M %p")} - {data.index[0].strftime("%I:%M %p")}) Close Prices and Volume')
        
        # fig.canvas.mpl_connect('figure_leave_event', on_focus_out)  # Close out after 15 minutes i fout of focus

        # Display the plot
        plt.show()
    
    # def get_holidays(self, year):
    #     '''
    #     Get the trading holidays for a given year
    #     year: int
    #     '''
    #     if datetime(year, 1, 1).weekday() == 5:
    #         new_years_day = datetime(year, 1, 3)
    #     elif datetime(year, 1, 1).weekday() == 6:
    #         new_years_day = datetime(year, 1, 2)
    #     else:
    #         new_years_day = datetime(year, 1, 1) 
    #     martin_luther_king_day = new_years_day + timedelta(days=(14 - new_years_day.weekday()))
    #     presidents_day = new_years_day + timedelta(days=(42 - new_years_day.weekday()))
    #     good_friday = new_years_day + timedelta(days=(70 - new_years_day.weekday()))
    #     memorial_day = new_years_day + timedelta(days=(91 - new_years_day.weekday()))
    #     if year >= 2021:
    #         juneteenth = datetime(year, 6, 19)
    #     else:
    #         juneteenth = None
    #     independence_day = datetime(year, 7, 4)
    #     if datetime(year, 7, 4).weekday() == 5:
    #         independence_day = datetime(year, 7, 5)
    #     elif datetime(year, 7, 4).weekday() == 6:
    #         independence_day = datetime(year, 7, 6)
    #     labor_day = new_years_day + timedelta(days=(252 - new_years_day.weekday()))
    #     thanksgiving_day = new_years_day + timedelta(days=(326 - new_years_day.weekday())) 
    #     christmas_day = datetime(year, 12, 25)
    #     holidays = [
    #         new_years_day,
    #         martin_luther_king_day,
    #         presidents_day,
    #         good_friday,
    #         memorial_day,
    #         juneteenth,
    #         independence_day,
    #         labor_day,
    #         thanksgiving_day,
    #         christmas_day
    #     ]
    #     if year < 2021:
    #         holidays.remove(juneteenth)
        
    #     return holidays
        
    def simulate_day(self, ticker, day, trading_strategy, month_data, start_time, end_time):
        '''
        Simulate a day of trading
        ticker: str
        day: str (YYYY-MM-DD)
        trading_strategy: function
        '''
        MY = day.split('-')[0:2]
        MY_str = '-'.join(MY)
        
        # If the month_data exists in a CSV file, load it. Otherwise, make the API request
        # Path of data: skew-bot/data/stocks/{ticker}/{year}/{month}.csv
        if month_data == None:
            try:
                month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                # print("Loaded data from CSV")
            except:
                try: 
                    month_data = self.load_data(
                        function='TIME_SERIES_INTRADAY',
                        symbol=ticker,
                        interval='1min',
                        month=MY_str,
                        outputsize='full'
                    )
                    
                    try: 
                        os.makedirs(f'data/stocks/{ticker}')
                    except:
                        pass
                        #print("Directories already exist or could not be created")
                    try:
                        os.makedirs(f'data/stocks/{ticker}/{MY[0]}')
                    except:
                        pass
                        #print("Directories already exist or could not be created")
                    month_data.to_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    try:
                        month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    except:
                        return "Could not load data from CSV"
                except:
                    return "No data found or API call limit recieved"
        
        day_data = None

        day = datetime.strptime(day, '%Y-%m-%d').strftime('%Y-%m-%d')
        for i in range(len(month_data)):
            if month_data['Unnamed: 0'][i].split(" ")[0] == day:
                day_data = month_data.iloc[i:]
                break
        if day_data is None:
            return "No data found for the day"
        
        start_time = datetime.strptime(day + ' ' + start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(day + ' ' + end_time, '%Y-%m-%d %H:%M:%S')
        is_trading = False
        trailing_data = pd.DataFrame()
        previous_price = 0
        initial_index = day_data.index[0]
        for i in range(len(day_data)):
            minute = day_data['Unnamed: 0'][i+initial_index]
            minute = datetime.strptime(minute, '%Y-%m-%d %H:%M:%S')
            if minute == start_time:
                is_trading = True
            if is_trading:
                if minute == end_time:
                    break
                if trading_strategy:
                    '''
                    trading_strategy should be a function that takes in one of the following:
                    ---------------------------
                    - ticker: str
                    - day_data: pandas DataFrame
                    - trailing_data: pandas DataFrame
                    - i: int
                    - minute: datetime
                    ---------------------------
                    - ticker: str
                    - previous_price: float
                    - current_price: float
                    ---------------------------
                    returns: void
                    '''
                    current_price = day_data['4. close'][i+initial_index]
                    try:
                        trading_strategy(ticker, day_data, trailing_data, i+initial_index, minute)
                    except:
                        try:
                            if previous_price != 0:
                                trading_strategy(ticker, previous_price, current_price)
                        except:
                            return "Trading strategy failed"


                trailing_data = trailing_data.append(day_data.iloc[i+initial_index])
                previous_price = trailing_data['4. close'][i+initial_index]
                

    



    def get_price(self, ticker, day, time, month_data=None):
        '''
        Get the price of a stock at a given time
        ticker: str
        day: str (YYYY-MM-DD)
        time: str (HH:MM:SS)
        '''
        MY = day.split('-')[0:2]
        MY_str = '-'.join(MY)
        
        # If the month_data exists in a CSV file, load it. Otherwise, make the API request
        # Path of data: skew-bot/data/stocks/{ticker}/{year}/{month}.csv
        if month_data == None:
            try:
                month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                # print("Loaded data from CSV")
            except:
                try: 
                    month_data = self.load_data(
                        function='TIME_SERIES_INTRADAY',
                        symbol=ticker,
                        interval='1min',
                        month=MY_str,
                        outputsize='full'
                    )
                    
                    try: 
                        os.makedirs(f'data/stocks/{ticker}')
                    except:
                        print("Directories already exist or could not be created")
                    try:
                        os.makedirs(f'data/stocks/{ticker}/{MY[0]}')
                    except:
                        print("Directories already exist or could not be created")
                    month_data.to_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    try:
                        month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    except:
                        return "Could not load data from CSV"
                except:
                    return "No data found or API call limit recieved"
        
        day_data = None

        day = datetime.strptime(day, '%Y-%m-%d').strftime('%Y-%m-%d')
        for i in range(len(month_data)): # Index col is index num, first col is date
            if month_data['Unnamed: 0'][i].split(" ")[0] == day:
                day_data = month_data.iloc[i:]
                break
        if day_data is None:
            return "No data found for the day"
            

        purchase_time = datetime.strptime(day + ' ' + time, '%Y-%m-%d %H:%M:%S')

        purchase_price = 0
        initial_index = day_data.index[0]
        for i in range(len(day_data)):
            minute = day_data['Unnamed: 0'][i+initial_index]
            minute = datetime.strptime(minute, '%Y-%m-%d %H:%M:%S')
            if minute == purchase_time:
                purchase_price = day_data['4. close'][i+initial_index]
                break
        return purchase_price

    def get_day_range(self, ticker, day, month_data=None):
        '''
        Get the average high low for each minute of the day from start to end time
        '''
        MY = day.split('-')[0:2]
        MY_str = '-'.join(MY)

        # If the month_data exists in a CSV file, load it. Otherwise, make the API request
        # Path of data: skew-bot/data/stocks/{ticker}/{year}/{month}.csv
        if month_data == None:
            try:
                month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                # print("Loaded data from CSV")
            except:
                try: 
                    month_data = self.load_data(
                        function='TIME_SERIES_INTRADAY',
                        symbol=ticker,
                        interval='1min',
                        month=MY_str,
                        outputsize='full'
                    )
                    
                    try: 
                        os.makedirs(f'data/stocks/{ticker}')
                    except:
                        print("Directories already exist or could not be created")
                    try:
                        os.makedirs(f'data/stocks/{ticker}/{MY[0]}')
                    except:
                        print("Directories already exist or could not be created")
                    month_data.to_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    try:
                        month_data = pd.read_csv(f'data/stocks/{ticker}/{MY[0]}/{MY[1]}.csv')
                    except:
                        return "Could not load data from CSV"
                except:
                    return "No data found or API call limit recieved"
            

        day = datetime.strptime(day, '%Y-%m-%d').strftime('%Y-%m-%d')
        day_data = None
        for i in range(len(month_data)):
            if month_data['Unnamed: 0'][i].split(" ")[0] == day:
                day_data = month_data.iloc[i:]
                break
       

    

# m = Market()
# # Example usage:
# data = m.load_data(
#     function='TIME_SERIES_INTRADAY',
#     symbol='TSLA',
#     interval='1min',
#     # month='2023-09'
#     # outputsize='full'
# )
# print(data)
# m._view(data)

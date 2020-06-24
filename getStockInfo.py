import requests
import json
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
from bokeh.embed import file_html, json_item
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource

#This is the API from which all our stock info will be retrieved
main_api = "https://www.alphavantage.co/query?"

#getthe closing price data for the user-inputted ticker symbol
#using the above API. Then put the info into a df using pandas.
def getClosingPrice(ticker):
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": str(ticker),
        "outputsize": "compact",
        "apikey": "UKVUZPKSXB2AP8M9"
    }

    #make sure the user has provided a valid ticker symbol and then proceed
    response = requests.get("https://www.alphavantage.co/query?", params=parameters)
    raw_data = response.content.decode("utf-8")
    if 'Error Message' in raw_data:
        errormessage = f'Sorry, {ticker} is not a valid ticker symbol'
        return errormessage
    else:
        data = json.loads(raw_data)
        df_wide = pd.DataFrame(data['Time Series (Daily)'])
        df_long = df_wide.transpose()
        df = pd.DataFrame(df_long['4. close']) #create df from closing price data
        df['close'] = df.loc[:,['4. close']].astype(float) #convert to numerical
        df['date'] = pd.to_datetime(df.index) #create datetime index
        return df

# create a plot out of the closing data dataframe
def plotStock(ticker):
    closingdata = getClosingPrice(ticker)

    #check to make sure that data has actually been retrieved
    if 'Sorry' in str(closingdata):
        return closingdata
        # return f'Sorry, {ticker} is not a valid ticker symbol'
    else:
        cds = ColumnDataSource(closingdata)
        # #create a static HTML file
        # output_file("plot.html")

        # create a plot with a title and axis labels
        plot = figure(title="Price for last 30 days", x_axis_label='day', y_axis_label='closing price')

        # add a line renderer with legend and line thickness
        plot.line(x='date', y='close', source = cds, line_width=2)

        # show(plot) #This will open up the plot in a new tab; this DOES work, if clunky

        # save(plot, "plot.html") #This will create an html document which supposedly contains the plot

        return plot
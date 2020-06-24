from flask import Flask, render_template, request, redirect
from getStockInfo import *
from bokeh.embed import components

app = Flask(__name__)

app.vars={}

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stocks')
def stocks():
  error = ""
  return render_template('stockview.html', errormessage=error)

@app.route('/displaystock', methods=['POST'])
def displaystock():
  userticker = request.form['tickersymbol']

  #first check that the ticker symbol is valid, then proceed
  if 'Sorry' in getClosingPrice(userticker):
    error = "that is not a valid ticker symbol"
    return render_template('stockview.html', errormessage=error)
  else:
    closingplot = plotStock(userticker)
    script, div = components(closingplot)
    return render_template('fig.html', stock=userticker, script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
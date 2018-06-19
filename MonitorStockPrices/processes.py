import json
import requests
import datetime
from emailScript import *

#Report Var
report = """"""

#Get Quote for Stock
def get_quote(ticker):
    #Robinhood API
    fund_link = "https://api.robinhood.com/fundamentals/" + ticker + "/"
    quote_link = "https://api.robinhood.com/quotes/" + ticker + "/"
    #Get Data
    fund_rsp = requests.get(fund_link)
    quote_rsp = requests.get(quote_link)
    if fund_rsp.status_code in (200,):
        fund_data = json.loads(fund_rsp.content.decode('unicode_escape'))
    if quote_rsp.status_code in (200,):
        quote_data = json.loads(quote_rsp.content.decode('unicode_escape'))
    #Results Dictionary
    results = {}
    results['ticker'] = ticker
    results['op'] = fund_data["open"]
    results['cp'] = quote_data['last_trade_price']
    return results
#Add Message to Report
def add_message_text(msg):
    global report
    report += msg
#Get a Single Report
def get_single_report(ticker):
    quote = get_quote(ticker)
    msg_txt = """
    Ticker: {}
    Opening Price: {}
    Current Price: {}
    Differential {} ({}%)
    """
    cp = quote['cp'].replace(",", "")
    op = quote['op'].replace(",", "")
    diffNum = float(cp) - float(op)
    diffPerc = (diffNum/float(cp)) * 100
    diffPerc = "{0:.2f}".format(diffPerc)
    diffStr = str(diffNum)
    if(diffNum > 0):
        diffStr = "+" + diffStr
    add_message_text(msg_txt.format(ticker, quote['op'], quote['cp'], diffStr, diffPerc))
#Get Full Report
def get_full_report(portfolio, watchList):
    global report
    report = ""
    portfolio_txt = """
    Portfolio Open: {}
    Portfolio Value: {}
    Differential {} ({}%)
    """
    portfolio_open = portfolio['Portfolio']
    portfolio_value = portfolio['Cash']
    #Determine Portoflio Value
    for ticker, qty in portfolio.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            temp_report = get_quote(ticker)
            value = float(temp_report['cp'].replace(",", "")) * float(qty)
            portfolio_value += value
        #Determine Differential in Portfolio Value
        diffNum = float(portfolio_value) - float(portfolio_open)
        diffPerc = (diffNum/float(portfolio_open)) * 100
        diffPerc = "{0:.2f}".format(diffPerc)
        diffStr = str(diffNum)
        if(diffNum > 0):
            diffStr = "+" + diffStr
    add_message_text(portfolio_txt.format(portfolio_open, portfolio_value, diffStr, diffPerc))
    #Holdings
    add_message_text("\nHoldings:\n")
    for ticker, holdings in portfolio.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            get_single_report(ticker)
    #WatchList
    add_message_text("\nWatch List:\n")
    for ticker, holdings in watchList.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            get_single_report(ticker)
    #Send report and return
    send_report(report)
    return portfolio_value
#Send report
def send_report(msg):
    subj = "Stock Report: " + datetime.date.today().strftime("%m-%d-%Y")
    msg_txt = msg
    print(msg_txt)
    send_stock_report(subj, msg_txt)

#Alert Stock
#Check quote and send alert if stock has reached upper threshold
def upper_threshold_alert(ticker, thresholds):
    report = get_quote(ticker)
    cp = report['cp'].replace(",", "")
    price = float(cp)
    if(thresholds["UpperThreshold"] >= price):
        return False;
    #Alert Threshold
    msg_txt = """
    Upper Threshold Reached
    Ticker: {}
    Current Price: {}
    """
    subj = "{} Threshold Alert"
    send_stock_report(subj.format(report['ticker']), msg_txt.format(report['ticker'], report['cp']))
    upperThreshold = price * 1.05
    lowerThreshold = price - (price * .05)
    thresholds = {}
    thresholds['upperThreshold'] = upperThreshold
    thresholds['lowerThreshold'] = lowerThreshold
    return thresholds;
#Check quote and send alert if stock has reached lower threshold
def lower_threshold_alert(ticker, thresholds):
    
    report = get_quote(ticker)
    cp = report['cp'].replace(",", "")
    price = float(cp)
    if(price >= thresholds["LowerThreshold"]):
        return False;
    #Alert Threshold
    msg_txt = """
    Lower Threshold Reached
    Ticker: {}
    Current Price: {}
    """
    subj = "{} Threshold Alert"
    send_stock_report(subj.format(report['ticker']), msg_txt.format(report['ticker'], report['cp']))
    upperThreshold = price * 1.05
    lowerThreshold = price - (price * .05)
    thresholds = {}
    thresholds['upperThreshold'] = upperThreshold
    thresholds['lowerThreshold'] = lowerThreshold
    return thresholds;

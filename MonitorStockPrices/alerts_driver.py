import time
from processes import *

#Lists
portfolioList = {}
watchList = {}

#Get Thresholds
def getThresholds():
    global portfolioList
    global watchList
    #On Server: '/root/Scripts/Stocks/Lists/portfolio.txt'
    with open("Lists/portfolio.txt") as _portfolio_file:
        for line in _portfolio_file:
            _temp_line = line.rstrip('\n')
            if(_temp_line[0] != "#" ):
                ticker, holdings, upperThreshold, lowerThreshold = _temp_line.split('|')
                if(ticker != 'Portfolio' and ticker != 'Cash'):
                    upperThreshold = float(upperThreshold)
                    lowerThreshold = float(lowerThreshold)
                portfolioList[ticker] = {"Holdings": holdings, "UpperThreshold": upperThreshold,
                "LowerThreshold": lowerThreshold}
    _portfolio_file.close()
    #On Server: '/root/Scripts/Stocks/Lists/watchlist.txt'
    with open("Lists/watchlist.txt") as _watchlist_file:
        for line in _watchlist_file:
            _temp_line = line.rstrip('\n')
            if(_temp_line[0] != "#"):
                ticker, upperThreshold, lowerThreshold = _temp_line.split('|')
                upperThreshold = float(upperThreshold)
                lowerThreshold = float(lowerThreshold)
                watchList[ticker] = {"UpperThreshold": upperThreshold, "LowerThreshold": lowerThreshold}
    _watchlist_file.close()
#Update Thresholds
def updateThresholds():
    global portfolioList
    global watchList
    #Portfolio List:
    #On Server: '/root/Scripts/Stocks/Lists/portfolio.txt'
    _portfolioList_writer = open('Lists/portfolio.txt', 'w')
    _portfolioList_writer.write('#Ticker|Holding Qty|Upper Threshold|Lower Threshold\n')
    for ticker, values in portfolioList.items():
        _portfolioList_writer.write(ticker + '|' + str(values["Holdings"]) + '|' +
        str(values["UpperThreshold"]) + '|' + str(values["LowerThreshold"]) + '\n')
    _portfolioList_writer.close()

    #Watch List:
    #On Server: '/root/Scripts/Stocks/Lists/watchlist.txt'
    _watchList_writer = open('Lists/watchlist.txt', 'w')
    _watchList_writer.write('#Ticker|Upper Threshold|Lower Threshold\n')
    for ticker, values in watchList.items():
        _watchList_writer.write(ticker + '|' + str(values["UpperThreshold"]) + '|' +
        str(values["LowerThreshold"]) + '\n')
    _watchList_writer.close()
#Main
def main():
    global portfolioList
    global watchList
    getThresholds()
    #Upper
    for ticker, thresholds in portfolioList.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            res = upper_threshold_alert(ticker, thresholds)
            if(res != False):
                portfolioList[ticker] = {"UpperThreshold": res['upperThreshold'],
                "LowerThreshold": res['lowerThreshold']}
    for ticker, thresholds in watchList.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            res = upper_threshold_alert(ticker, thresholds)
            if(res != False):
                watchList[ticker] = {"UpperThreshold": res['upperThreshold'],
                "LowerThreshold": res['lowerThreshold']}
    #Lower
    for ticker, thresholds in portfolioList.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            res = lower_threshold_alert(ticker, thresholds)
            if(res != False):
                portfolioList[ticker] = {"UpperThreshold": res['upperThreshold'],
                "LowerThreshold": res['lowerThreshold']}
    for ticker, thresholds in watchList.items():
        if(ticker != 'Portfolio' and ticker != 'Cash'):
            res = lower_threshold_alert(ticker, thresholds)
            if(res != False):
                watchList[ticker] = {"UpperThreshold": res['upperThreshold'],
                "LowerThreshold": res['lowerThreshold']}
    updateThresholds()
if __name__ == '__main__':
    main()

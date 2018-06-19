from processes import *
#Get Report List
def getReportList():
    portfolioList = {}
    watchList = {}
    result = {}
    #On Server: '/root/Scripts/Stocks/Lists/portfolio.txt'
    with open("Lists/portfolio.txt") as _portfolio_file:
        for line in _portfolio_file:
            _temp_line = line.rstrip('\n')
            if(_temp_line[0] != "#"):
                ticker, holdings, upperThreshold, lowerThreshold = _temp_line.split('|')
                holdings = float(holdings)
                portfolioList[ticker] = holdings
    _portfolio_file.close()
    #On Server: '/root/Scripts/Stocks/Lists/watchlist.txt'
    with open("Lists/watchlist.txt") as _watchlist_file:
        for line in _watchlist_file:
            _temp_line = line.rstrip('\n')
            if(_temp_line[0] != "#"):
                ticker, upperThreshold, lowerThreshold = _temp_line.split('|')
                watchList[ticker] = ticker
    _watchlist_file.close()
    result["Portfolio"] = portfolioList
    result["WatchList"] = watchList
    return result
def update_portfolio(value):
    #On Server: "/root/Scripts/Stocks/Lists/portfolio.txt"
    with open("Lists/portfolio.txt", 'r') as _portfolio_file:
        data = _portfolio_file.readlines()
    i = 0
    for line in data:
        _temp_line = line.rstrip('\n')
        ticker, holdings, upperThreshold, lowerThreshold = _temp_line.split('|')
        if(ticker == "Portfolio"):
            data[i] = "Portfolio|" + str(value) +"|null|null"
        i += 1
    #On Server: "/root/Scripts/Stocks/Lists/portfolio.txt"
    with open("Lists/portfolio.txt", 'w') as _portfolio_file:
        _portfolio_file.writelines(data)
#Main
def main():
    result = getReportList()
    value = get_full_report(result["Portfolio"], result["WatchList"])
    update_portfolio(value)
if __name__ == '__main__':
    main()

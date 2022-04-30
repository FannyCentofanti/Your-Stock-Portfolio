from helpers import get_stock_price, get_stock_info

# class to create the needed stock data for each user.

class user_stock_data:
    def __init__(self, symbol, shares):

        stock_info = get_stock_info(symbol)
        stock_value = get_stock_price(symbol)

        if stock_info == None:
            return None

        self.symbol = symbol
        self.company_name = stock_info['name']
        self.industry = stock_info['industry']
        self.sector = stock_info['sector']
        self.shares = int(shares)
        if stock_value != None:
            self.current_stock_value = round(stock_value, 3)
            self.total_value = round(self.shares * self.current_stock_value, 3)
        else:
            self.current_stock_value = "NaN"
            self.total_value = "NaN"
        

    def encode(self):
        return self.__dict__


def get_total_value(portfolio):
    '''Calculate the total value of the user portfolio'''

    total_value = 0

    for row in portfolio:
        if row == None:
            continue
        if row.total_value == "NaN":
            continue
        total_value += row.total_value

    return total_value

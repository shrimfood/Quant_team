from pykrx import stock
import pandas as pd
import numpy as np

def choose_func(date, *data):
    b_day = stock.get_nearest_business_day_in_a_week(date)
    price_data = price_data = stock.get_market_fundamental_by_ticker(b_day, market='ALL')
    return price_data[list(data)]

def date_func(date):
    b_day = stock.get_nearest_business_day_in_a_week(date)
    return b_day


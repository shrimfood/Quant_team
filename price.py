from pykrx import stock
import pandas as pd
import numpy as np

def price_func(date, date2):
    codes_kospi = stock.get_market_ticker_list(date, market='KOSPI') # 코스피, 코스닥 데이터의 종목코드 데이터
    codes_kosdaq = stock.get_market_ticker_list(date, market='KOSDAQ')
    codes = []
    for i in range(len(codes_kospi)):
        codes.append(codes_kospi[i])
    for i in range(len(codes_kosdaq)):
        codes.append(codes_kosdaq[i])

    corp = []
    for code in codes:
        name = stock.get_market_ticker_name(code) # 코스피, 코스닥 데이터의 종목명 데이터
        corp.append([code, name])
    df1 = pd.DataFrame(data=corp, columns=['티커', '종목명'])
    df1 = df1.set_index('티커') # 종목코드 인덱스화 

    list = []
    for i in range(len(df1)):
        if '스팩' in df1['종목명'][i] or df1.index[i][-1] != '0':
            list.append(df1.index[i])
    df1 = df1.drop(list, axis=0)

    df_kospi = stock.get_market_cap_by_ticker(date=date, market='KOSPI')  # 코스피 종가 
    df_kosdaq = stock.get_market_cap_by_ticker(date=date, market='KOSDAQ') # 코스닥 종가
    df = pd.concat([df_kospi, df_kosdaq])
    df = df.drop(['시가총액','거래대금'], axis=1)

    df_kospi_1= stock.get_market_cap_by_ticker(date=date2, market='KOSPI')  # 1년 후 코스피 종가
    df_kosdaq_1 = stock.get_market_cap_by_ticker(date=date2, market='KOSDAQ')  
    df_1 = pd.concat([df_kospi_1, df_kosdaq_1])
    df_1 = df_1.drop(['시가총액', '거래량', '거래대금'], axis=1)

    df_total = pd.merge(df, df_1, how='left', on=['티커'])
    df_total = pd.merge(df1, df_total, how='left', on=['티커'])
    df_total.columns = ['종목명', '종가', '거래량', '상장주식수', '1년후종가', '1년후상장주식수']
    df_total['상장주식수변동'] = df_total['1년후상장주식수'] - df_total['상장주식수']

    return df_total
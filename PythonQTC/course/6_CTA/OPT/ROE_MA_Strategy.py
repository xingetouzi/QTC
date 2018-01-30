import numpy as np
import talib as ta
import pandas as pd
import rqalpha
from rqalpha.api import *

stock_df = pd.read_excel('roe_backtest.xlsx')


#读取文件位置
def init(context):
    context.codes = stock_df
    context.stocks = []
    context.SHORTPERIOD = 20
#     scheduler.run_weekly(find_pool, tradingday=1)
    scheduler.run_daily(find_pool)

def find_pool(context, bar_dict):
    try:
        codes = context.codes.loc[context.now]
    except KeyError:
        return
    stocks = codes.index[codes == 1]
    context.stocks = stocks

def handle_bar(context, bar_dict):
    buy(context, bar_dict)
    
    
def buy(context, bar_dict):
    pool = context.stocks
#     print (pool)
    if pool is not None:
        stocks_len = len(pool)
        for stocks in context.portfolio.positions:
            if stocks not in pool:
                order_target_percent(stocks, 0)
        for codes in pool:
            try:
                price = history_bars(codes, context.SHORTPERIOD+10, '1d', 'close')
                short_avg = ta.SMA(price, context.SHORTPERIOD)
                cur_position = context.portfolio.positions[codes].quantity
                if short_avg[-1]<short_avg[-3] and cur_position > 0:
                    order_target_value(codes, 0)
                if short_avg[-1]  > short_avg[-3]:
                    order_target_percent(codes, 1.0/stocks_len)
            except Exception:
                pass


config = {
  "base": {
    "start_date": "2015-09-01",
    "end_date": "2017-12-30",
    "accounts": {'stock':1000000},
    "benchmark": "000300.XSHG"
  },
  "extra": {
    "log_level": "error",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

if __name__ == "__main__":
    rqalpha.run_func(init=init, handle_bar=handle_bar, config=config)
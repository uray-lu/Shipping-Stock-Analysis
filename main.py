#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 15:28:31 2022

@author: ray
"""


#Require packages 

from Data.get_close_price import GetStockData
from Preprocess.preprocess import MakePlot, ACF, PACF, ADF_test, Ljung_box_test 
from Model.var_model import ModelConstruct



#%%

# Get Close Price

stock_lists = ['2609.TW', '2603.TW', '2615.TW', '5608.TW', '2605.TW','2606.TW', '2637.TW' ]
stocks_data = GetStockData('2021-01-01', '2022-01-01', stock_lists)
stocks = stocks_data.MakeOutPut()

# first order difference as first difference

stocks_diff = stocks.diff().dropna()
stocks_diff = stocks_diff.rename(columns = {'2609.TW':'2609.TW Diff', '2603.TW':'2603.TW Diff', '2615.TW':'2615.TW Diff', '5608.TW':'5608.TW Diff', '2605.TW':'2605.TW Diff','2606.TW':'2606.TW Diff', '2637.TW':'2637.TW Diff' })

#%%
# Plot Original Price

for i in stock_lists:
    
    MakePlot(stocks, i, 0)
    ACF(stocks, i, 0)
    PACF(stocks, i, 0)


# Plot first Diff Price

for i in stocks_diff.columns:
    
    MakePlot(stocks_diff, i, 1)
    ACF(stocks_diff, i, 1)
    PACF(stocks_diff, i, 1)


#ADF test for stocks raw data

ADF_test(stocks)

#ADF test for stocks first Diff data

ADF_test(stocks_diff)


# Ljun-box test for stocks raw data

stocks_lb_test = Ljung_box_test(stocks)

# Ljun-box test for stocks Diff

stocks_returns_lb_test = Ljung_box_test(stocks_diff)



# Model Construction

test_obs = int(len(stocks_diff)*0.2)
train_data = stocks_diff[:-test_obs]
test_data = stocks_diff[-test_obs:]

# Model construction
#%%
container = ModelConstruct(train_data, 'container')
bulk = ModelConstruct(train_data, 'bulk')
all_stocks = ModelConstruct(train_data, 'all')


#Search for the order for VAR model

container_order = container.GridsearchforP()
bulk_order = bulk.GridsearchforP()
all_stocks_order = all_stocks.GridsearchforP()


#fit three VAR() model

Model_container = container.Model(4)
Model_bulk = bulk.Model(1) 
Model_all = all_stocks.Model(1)

#Forecast

container_forecast = container.Forecast(4,stocks, test_data)
bulk_forecast = bulk.Forecast(1, stocks, test_data)
all_stocks_forecast  =all_stocks.Forecast(1, stocks,  test_data)






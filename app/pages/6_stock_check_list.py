import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
#Data Source
# import yfinance as yf

#Data viz
import plotly.graph_objs as go
import requests

st.set_page_config(layout="wide")

st.header(':orange[STOCK infor!]')

st.header('')
            
import os

fix_stock = st.multiselect("Please select numbers", ['TLRY','NIO','TSLA','TGT','AMC','RBLX','PLTR','XLK','UDMY','BAC','DAL','AAL','SHOP','UBER','NVDA'])
# st.write(fixed_numbers)
def volume_by_ticker(ticker_list):
    col1,col2 = st.columns(2)
    # data = yf.download(tickers=ticker, period=str(round(days_back,0))+'d', interval='1d').reset_index()
    for i in  range(len(ticker_list)):
        ticker=ticker_list[i]

        data = yf.download(tickers=ticker, period='1d', interval='1m')

        #declare figure
        fig = go.Figure()

        #Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],             
                        name = 'market data'))
        #    volume=data['Volume'],
        # Add titles
        fig.update_layout(
            title=f'{ticker} live share price evolution',
            yaxis_title='Stock Price (USD per Shares)')

        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        if i % 2 ==0:
    
            with col1:
                st.plotly_chart(fig)
                st.write(data.tail(5))
        else:
            with col2:
                st.plotly_chart(fig)
                st.write(data.tail(5))
    # fig.show()

submited=st.button('Refresh')
#Interval required 5 minutes
if submited:
    # ticker_list=['TLRY','NIO','TSLA','TGT','AMC','RBLX','PLTR','XLK','UDMY','BAC','DAL','AAL','SHOP','UBER','NVDA']
    ticker_list=fix_stock
    
    volume_by_ticker(ticker_list)

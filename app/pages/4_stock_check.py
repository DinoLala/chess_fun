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

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
import requests

st.set_page_config(layout="wide")

st.header(':orange[STOCK infor!]')

st.header('')
            
import os
def volume_by_ticker(ticker):
    data = yf.download(tickers=ticker, period='1d', interval='5m')

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
    # st.pyplot(fig) 
    st.plotly_chart(fig)
    # fig.show()
def plot_ticker(df_temp, metric_plot,ticker):
    two_subplot_fig = plt.figure(figsize=(6,6),facecolor='lightblue')
    plt.subplot(211)
    plt.plot(df_temp['Date'] ,df_temp[metric_plot] , color='tab:orange', marker='.')
    # plt.subplot(212)
    # plt.plot(df_temp['End_event_date'] ,df_temp['quick_rating'] , color='tab:blue', marker='.')
    plt.xticks(rotation=30)
    # x_stick=[df_temp['End_event_date'][i] for i  in range(len(df_temp['End_event_date'])) if i%5 == 0 ]
    # plt.xticks(x_stick)
    plt.grid()
    plt.title(f' {ticker} trend -{metric_plot}')
    st.pyplot(two_subplot_fig)


# --------------------------------------------------
col1,col2 = st.columns(2)
common_list=['TLRY','NIO','TSLA','TGT','AMC','RBLX','PLTR','XLK','UDMY','BAC','DAL','AAL']
with col1:
    ticker=st.selectbox( 'TICKER',common_list)
    days_back=st.selectbox( 'Days back',[30,5,10,20,30,60,120,180])
    # st.text_input('Ticker' ,value='NIO')
with col2:
    metric_plot=st.selectbox( 'metric_plot',['Volume','Close'])
    metric_plot2=st.selectbox( 'metric_plot',['Close','Volume'])
#Interval required 5 minutes
data = yf.download(tickers=ticker, period=str(round(days_back,0))+'d', interval='1d').reset_index()
#Print data

print(data['Date'].max())
volume_by_ticker(ticker)
col1,col2 = st.columns(2)

with col1:
    plot_ticker(data,metric_plot,ticker)
with col2:
    plot_ticker(data,metric_plot2,ticker)
data=data.sort_values(by='Date', ascending=False)
st.write(data)
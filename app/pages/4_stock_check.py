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
def volume_by_ticker(ticker):
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
    # st.pyplot(fig) 
    col1,col2 = st.columns(2)
    with col1:
        st.write(data.tail())
    with col2:
        st.plotly_chart(fig)
    # fig.show()
def plot_ticker(df_temp, metric_plot,ticke,show_bollingerr):
    two_subplot_fig = plt.figure(figsize=(6,6),facecolor='lightblue')
    plt.subplot(211)
    plt.plot(df_temp['Date'] ,df_temp[metric_plot] , color='tab:orange', marker='.')
    
    plt.plot(df_temp['Date'] ,df_temp[metric_plot+'Moving_Avg'] , color='tab:purple',linestyle='dashed', marker='.')
    if show_bollinger =='yes':
        plt.plot(df_temp['Date'] ,df_temp[metric_plot+'Upper_Band'] , color='tab:red',linestyle='dashed')
        plt.plot(df_temp['Date'] ,df_temp[metric_plot+'Lower_Band'] , color='tab:green',linestyle='dashed')
    
    plt.xticks(rotation=30)
    plt.grid()
    plt.title(f' {ticker} trend -{metric_plot}')
    st.pyplot(two_subplot_fig)

# Function to get the earnings calendar for the current week
def get_earnings_calendar(ticker):
    today = datetime.now()
    start_date = today - timedelta(days=today.weekday())  # Monday of the current week
    end_date = start_date + timedelta(days=30)  # Friday of the current week

    # Fetch the earnings calendar
    earnings_calendar =      yf.Ticker(ticker).get_earnings_dates()
    print(earnings_calendar.columns)

    # Filter earnings within the current week
    earnings_this_week = earnings_calendar[
        (earnings_calendar.index >= start_date.strftime('%Y-%m-%d')) & 
        (earnings_calendar.index<= end_date.strftime('%Y-%m-%d'))
    ].reset_index()
    # st.write(earnings_this_week['Earnings Date'][0])
    from datetime import timezone
    date2=earnings_this_week['Earnings Date'][0].replace(tzinfo=timezone.utc).astimezone(tz=None)    
    difference = (date2 - today).days
    st.write(f':orange[Next earning date {date2.date()} in : {difference} days]')
    return earnings_this_week.head(5)
# --------------------------------------------------
metric_list=['Volume','Close']
col1,col2 = st.columns(2)
common_list=['TLRY','NIO','TSLA','TGT','AMC','RBLX','PLTR','XLK','UDMY','BAC','DAL','AAL','SHOP']
with col1:
    ticker=st.selectbox( 'TICKER',common_list)
    days_back=st.selectbox( 'Days back',[30,5,10,20,30,60,120,180])
    window_size =st.selectbox( 'moving avg',[5,10,20,60])
    # window_size = 3
    # st.text_input('Ticker' ,value='NIO')
with col2:
    metric_plot=st.selectbox( 'metric_plot',metric_list)
    metric_plot2=st.selectbox( 'metric_plot',['Close','Volume'])
    show_bollinger=st.selectbox( 'show bollinger band',['no','yes'])
#Interval required 5 minutes
data = yf.download(tickers=ticker, period=str(round(days_back,0))+'d', interval='1d').reset_index()


# Calculate the moving average
for c in metric_list:
    data[c+'Moving_Avg'] = data[c].rolling(window=window_size).mean()
    # Calculate the rolling standard deviation
    data[c+'Std_Dev'] = data[c].rolling(window=window_size).std()

    # Calculate the upper Bollinger Band
    data[c+'Upper_Band'] = data[c+'Moving_Avg'] + (data[c+'Std_Dev'] * 2)

    # Calculate the lower Bollinger Band
    data[c+'Lower_Band'] = data[c+'Moving_Avg'] - (data[c+'Std_Dev'] * 2)
#Print data
try:
    earnings_this_week = get_earnings_calendar(ticker)
except:
    pass
# st.write(earnings_this_week)

print(data['Date'].max())
volume_by_ticker(ticker)
col1,col2 = st.columns(2)

with col1:
    plot_ticker(data,metric_plot,ticker,show_bollinger)
with col2:
    plot_ticker(data,metric_plot2,ticker,show_bollinger)
data=data.sort_values(by='Date', ascending=False)
st.write(data)
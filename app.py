import yfinance as yf
import pandas as pd
import streamlit as st
# import plotly as plt

# https://github.com/ranaroussi/yfinance
# https://docs.streamlit.io/library/api-reference
# https://chat.openai.com/

st.sidebar.title("Finance App")

tickers_list = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT']
selected_ticker = st.sidebar.selectbox('Selecione uma ação', tickers_list)

st.sidebar.image('patinhas.png', use_column_width=True)

st.metric(label="Selected action:", value=selected_ticker)

st.header("News")
ticker_news = yf.Ticker(selected_ticker).news
news = pd.DataFrame.from_records(ticker_news)
news = news.drop(['uuid', 'providerPublishTime', 'thumbnail'], axis=1)
st.dataframe(news, use_container_width=True)

st.header("History")
ticker_history = yf.Ticker(selected_ticker).history(period='1mo')
st.dataframe(ticker_history, use_container_width=True)

st.header("Actions")
ticker_actions = yf.Ticker(selected_ticker).actions
st.dataframe(ticker_actions, use_container_width=True)

st.header("Splits")
ticker_splits = yf.Ticker(selected_ticker).splits
st.dataframe(ticker_splits, use_container_width=True)

st.header("Dividends")
ticker_dividends = yf.Ticker(selected_ticker).dividends
st.dataframe(ticker_dividends, use_container_width=True)

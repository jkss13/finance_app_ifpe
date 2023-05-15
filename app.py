# https://github.com/ranaroussi/yfinance
# https://docs.streamlit.io/library/api-reference
# https://chat.openai.com/

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

st.sidebar.title("Finance App")

tickers_list = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT']
selected_ticker = st.sidebar.selectbox('Selecione uma ação', tickers_list)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.image('patinhas.png', use_column_width=True)

st.metric(label="Selected action:", value=selected_ticker)

with st.expander("History"):
    st.subheader("Data")

    history_data = yf.Ticker(selected_ticker).history(period='1mo')
    history_data = history_data.reset_index()  # Resetando o índice para obter a coluna de datas
    st.dataframe(history_data, use_container_width=True)

    fig = go.Figure(data=[go.Candlestick(x=history_data['Date'],
                    open=history_data['Open'],
                    high=history_data['High'],
                    low=history_data['Low'],
                    close=history_data['Close'])])
    st.subheader("Candlesticks Chart")
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Actions"):
    st.subheader("Data")
    actions_data = yf.Ticker(selected_ticker).actions
    actions_data = actions_data.reset_index()  
    st.dataframe(actions_data, use_container_width=True)

with st.expander("Dividends"):
    st.subheader("Data")
    dividends_data = yf.Ticker(selected_ticker).dividends
    dividends_data = dividends_data.reset_index()  
    st.dataframe(dividends_data, use_container_width=True)

with st.expander("Splits"):
    st.subheader("Data")
    splits_data = yf.Ticker(selected_ticker).splits
    splits_data = splits_data.reset_index() 
    st.dataframe(splits_data, use_container_width=True)

with st.expander("News"):
    st.subheader("Data")
    news_data = yf.Ticker(selected_ticker).news
    news_data = pd.DataFrame.from_records(news_data)
    news_data = news_data.drop(['uuid', 'providerPublishTime', 'thumbnail'], axis=1)
    st.dataframe(news_data, use_container_width=True)
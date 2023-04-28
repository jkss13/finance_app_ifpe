import streamlit as st
import yfinance as yf

# https://github.com/ranaroussi/yfinance

st.sidebar.title("Finances App")

options = st.sidebar.multiselect(
    'Ações',
    ['FNF', 'ASML', 'GOOGL', 'AAPL'],
    ['MSFT'])

# input_action = st.sidebar.text_input("Ação: ")
# action_ticker = yf.Ticker(options)
# st.write(options.history(period="1mo"))
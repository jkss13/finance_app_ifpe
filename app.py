# https://github.com/ranaroussi/yfinance
# https://docs.streamlit.io/library/api-reference
# https://chat.openai.com/
# https://www.alphavantage.co/

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.title("Finance App")
tab1, tab2, tab3 = st.tabs(["Menu", "Segment Details", "Ticker Details"])
with tab1:
    segments = ["Technology"]
    segment = st.selectbox('Selecione um segmento', segments)
    # api_key = "JS0BP2SS4ZTC1RDW"
    # url = f"https://www.alphavantage.co/scan?function=LIST_ALL_TAGS&apikey={api_key}"
    # response = requests.get(url)
    # data = response.json()
    # topics = data["tags"]
    # st.write(topics)
with tab2:
    st.metric(label="Segment:", value=segment)
    url = f"https://finance.yahoo.com/sector/{segment.lower().replace(' ', '-')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows[1:]:
        ticker = row.find('td').text
        tickers.append(ticker)
    selected_ticker = st.selectbox('Selecione uma ação', tickers)
with tab3:
    st.metric(label="Ticker:", value=selected_ticker)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["History", "Actions", "Dividends", "Splits", "News"])
    with tab1:
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
    with tab2:
        st.subheader("Data")
        actions_data = yf.Ticker(selected_ticker).actions
        actions_data = actions_data.reset_index()  
        st.dataframe(actions_data, use_container_width=True)
        fig = px.line(actions_data, x='Date', y='Dividends')
        fig.update_layout(
            title='Dividend Fluctuation',
            xaxis_title='Ano',
            yaxis_title='Dividendos',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.subheader("Data")
        dividends_data = yf.Ticker(selected_ticker).dividends
        dividends_data = dividends_data.reset_index()  
        st.dataframe(dividends_data, use_container_width=True)
        fig = px.line(dividends_data, x='Date', y='Dividends')
        fig.update_layout(
            title='Dividend Fluctuation',
            xaxis_title='Ano',
            yaxis_title='Dividendos',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab4:
        st.subheader("Data")
        splits_data = yf.Ticker(selected_ticker).splits
        splits_data = splits_data.reset_index() 
        st.dataframe(splits_data, use_container_width=True)
        data_grouped = splits_data.groupby(splits_data['Date'].dt.year)['Stock Splits'].sum().reset_index()
        data_grouped.columns = ['Ano', 'Quantidade']
        fig = px.bar(data_grouped, x='Ano', y='Quantidade', labels={'Quantidade': 'Quantidade de Stock Splits'}, 
                title='Stock Splits Number by Year')
        fig.update_layout(xaxis={'type': 'category'})
        st.plotly_chart(fig, use_container_width=True)
    with tab5:
        st.subheader("Data")
        news_data = yf.Ticker(selected_ticker).news
        news_data = pd.DataFrame.from_records(news_data)
        news_data = news_data.drop(['uuid', 'providerPublishTime', 'thumbnail'], axis=1)
        st.dataframe(news_data, use_container_width=True)
        st.subheader("News by Related Tickers")
        counts = news_data.explode("relatedTickers").groupby(["relatedTickers", "title"]).size().unstack(fill_value=0)
        counts = counts.reset_index().melt(id_vars="relatedTickers", var_name="title", value_name="count")
        fig = px.bar(counts, x="relatedTickers", y="count", barmode="stack",
                labels={"relatedTickers": "Related Tickers", "count": "Quantidade de Itens"})
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("News by Publisher (%)")
        df_grouped = news_data.groupby('publisher')['title'].count().reset_index()
        df_grouped['percentage'] = (df_grouped['title'] / df_grouped['title'].sum()) * 100
        fig = px.pie(df_grouped, values='title', names='publisher', 
                    labels={'title': 'Amount', 'publisher': 'Publisher'}, 
                    title='Percentage of items per Publisher')
        st.plotly_chart(fig, use_container_width=True)
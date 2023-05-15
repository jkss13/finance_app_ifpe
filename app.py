# https://github.com/ranaroussi/yfinance
# https://docs.streamlit.io/library/api-reference
# https://chat.openai.com/

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px

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
    st.subheader("Chart")
    # dividends_data["Year"] = dividends_data["Date"].year
    fig = px.line(actions_data, x='Date', y='Dividends')
    fig.update_layout(
        title='Oscilação de Dividendos',
        xaxis_title='Ano',
        yaxis_title='Dividendos',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Dividends"):
    st.subheader("Data")
    dividends_data = yf.Ticker(selected_ticker).dividends
    dividends_data = dividends_data.reset_index()  
    st.dataframe(dividends_data, use_container_width=True)
    st.subheader("Chart")
    # dividends_data["Year"] = dividends_data["Date"].year
    fig = px.line(dividends_data, x='Date', y='Dividends')
    fig.update_layout(
        title='Oscilação de Dividendos',
        xaxis_title='Ano',
        yaxis_title='Dividendos',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Splits"):
    st.subheader("Data")
    splits_data = yf.Ticker(selected_ticker).splits
    splits_data = splits_data.reset_index() 
    st.dataframe(splits_data, use_container_width=True)
    st.subheader("Stock Splits Number by Year")
    data_grouped = splits_data.groupby(splits_data['Date'].dt.year)['Stock Splits'].sum().reset_index()
    data_grouped.columns = ['Ano', 'Quantidade']
    fig = px.bar(data_grouped, x='Ano', y='Quantidade', labels={'Quantidade': 'Quantidade de Stock Splits'}, 
             title='Quantidade de Stock Splits por Ano')
    # Configurar o layout do gráfico
    fig.update_layout(xaxis={'type': 'category'})
    st.plotly_chart(fig, use_container_width=True)

with st.expander("News"):
    st.subheader("Data")
    news_data = yf.Ticker(selected_ticker).news
    news_data = pd.DataFrame.from_records(news_data)
    news_data = news_data.drop(['uuid', 'providerPublishTime', 'thumbnail'], axis=1)
    st.dataframe(news_data, use_container_width=True)
    st.subheader("News by Tickers")
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
from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(layout="wide")

col1, col2= st.columns([1, 2])

with col1:
    st.header("Backtestr Prototype")
    with st.container():

        stockName = st.selectbox("Select Stock", ("---", "ADVANC", "AOT", "AWC", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC", "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"))

        if stockName != "---":
            ticker_symbol = stockName + ".bk"
            stock = yf.Ticker(ticker_symbol)
            data = stock.history(period="6mo").drop(columns=['Volume', 'Dividends', 'Stock Splits'])

            indicator = Indicator(data)
            strategy = Strategy(data)
            backtestr = Backtestr(data, ticker_symbol)

            if "data" not in st.session_state:
                st.session_state.data = data
                st.session_state.indicator = indicator
                st.session_state.strategy = strategy
                st.session_state.backtestr = backtestr

            st.dataframe(data, height=200)
            
            selectedIndicator = st.selectbox("Select Indicator", ("---", "MA", "EMA", "MACD", "RSI", "StochRSI"), key="input_indicator")
            if selectedIndicator in ["MA", "EMA", "RSI", "StochRSI"]:
                averageInterval = st.slider("Average Interval", min_value=1, max_value=100, step=1, value=20)
            if selectedIndicator in ["MACD"]:
                firstAverageInterval = st.slider("First Average Interval", min_value=1, max_value=100, step=1, value=12)
                secondAverageInterval = st.slider("Second Average Interval", min_value=1, max_value=100, step=1, value=26)
                signalAverageInterval = st.slider("Signal Average Interval", min_value=1, max_value=100, step=1, value=9)
                
                
            if st.button("Submit"):
                if selectedIndicator == "MA":
                    st.session_state.indicator.makeMA(averageInterval=averageInterval)
                if selectedIndicator == "EMA":
                    st.session_state.indicator.makeEMA(averageInterval=averageInterval)
                if selectedIndicator == "MACD":
                    st.session_state.indicator.makeMACD(firstAverageInterval=firstAverageInterval, secondAverageInterval=secondAverageInterval, signalAverageInterval=signalAverageInterval)
                if selectedIndicator == "RSI":
                    st.session_state.indicator.makeRSI(averageInterval=averageInterval)
                if selectedIndicator == "StochRSI":
                    st.session_state.indicator.makeStochRSI(averageInterval=averageInterval)


            with col2:
                indicatorList = st.session_state.indicator.getIndicatorList()
                options = st.multiselect(
                    "Indicator",
                    indicatorList
                )

                mainChart = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="Candlesticks",
                )])
                MACDChart = go.Figure()
                RSIChart = go.Figure()

                for indicatorName in options:
                    if "MACD" in indicatorName or "Signal" in indicatorName:
                        MACDChart.add_trace(go.Scatter(
                            x=st.session_state.data.index,
                            y=st.session_state.data[indicatorName],
                            mode='lines',
                            name=indicatorName
                        ))
                    elif "RSI" in indicatorName:
                        RSIChart.add_trace(go.Scatter(
                            x=st.session_state.data.index,
                            y=st.session_state.data[indicatorName],
                            mode='lines',
                            name=indicatorName
                        ))
                    elif "MA" in indicatorName:
                        mainChart.add_trace(go.Scatter(
                            x=st.session_state.data.index,
                            y=st.session_state.data[indicatorName],
                            mode='lines',
                            name=indicatorName
                        ))

                mainChart.update_layout(
                    title="Candlestick Chart",
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False,
                    height=440
                )

                MACDChart.update_layout(
                    title="MACD Chart",
                    xaxis_title='Date',
                    yaxis_title='MACD',
                    xaxis_rangeslider_visible=False,
                    height=440
                )

                RSIChart.update_layout(
                    title="RSI Chart",
                    xaxis_title='Date',
                    yaxis_title='RSI',
                    xaxis_rangeslider_visible=False,
                    height=440
                )

                st.write(mainChart)
                st.write(MACDChart)
                st.write(RSIChart)

from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(layout="wide")

st.header("Backtestr Prototype")

dataTab, graphTab, searchTab, docTab, featureRequestTab = st.tabs(["🗃 Data", "📈 Chart", "🔎 Stock Search", "📄 Documentation", "💡 Feature Request"])

with dataTab:
    dataTab_col1, dataTab_col2, dataTab_col3 = st.columns([1, 1, 1])
    with dataTab_col1:
        with st.container(border=True):
            stockCol, periodCol, intervalCol, downloadCol = st.columns([2, 1, 1, 1])
            with stockCol:
                stockName = st.selectbox("Select Stock", ("---", "ADVANC", "AOT", "AWC", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC", "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"))
            with periodCol:
                period = st.selectbox("Select Period", ("---", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"))
            with intervalCol:    
                interval = st.selectbox("Select Interval", ("---", "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo"))
            with downloadCol:
                st.write("######")
                downloadButton = st.button("Download", type="primary")

        if stockName != "---" and period != "---" and interval != "---":
            ticker_symbol = stockName + ".bk"
            stock = yf.Ticker(ticker_symbol)
            data = stock.history(period=period, interval=interval).reset_index(drop=True)

            st.dataframe(data, height=300, width=800)

    if downloadButton:
        indicator = Indicator(data)
        strategy = Strategy(data)

        st.session_state.data = data
        st.session_state.indicator = indicator
        st.session_state.strategy = strategy

    if "data" in st.session_state:
        with dataTab_col2:

            with st.popover("Add Indicator", use_container_width=True):
                selectedIndicator = st.selectbox("Select Indicator", ("---", "MA", "EMA", "MACD", "RSI", "StochRSI", "StochOscillator"), key="input_indicator")
                if selectedIndicator in ["MA", "EMA", "RSI", "StochRSI", "StochOscillator"]:
                    averageInterval = st.slider("Average Interval", min_value=1, max_value=100, step=1, value=20)
                if selectedIndicator in ["MACD"]:
                    firstAverageInterval = st.slider("First Average Interval", min_value=1, max_value=100, step=1, value=12)
                    secondAverageInterval = st.slider("Second Average Interval", min_value=1, max_value=100, step=1, value=26)
                    signalAverageInterval = st.slider("Signal Average Interval", min_value=1, max_value=100, step=1, value=9)
                    
                if st.button("Add Indicator"):
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
                    if selectedIndicator == "StochOscillator":
                        st.session_state.indicator.makeStochOscillator(averageInterval=averageInterval)
            
            with st.container(border=True):
                st.write(st.session_state.indicator)

            with st.popover("Add Strategy", use_container_width=True):
                selectedStrategy = st.selectbox("Select Strategy", ("---", "Cross Over", "Boundary"))
                indicatorList = st.session_state.indicator.getIndicatorList()
                if selectedStrategy == "Cross Over":
                    column1, column2 = st.columns([1, 1])
                    with column1:
                        firstLine = st.selectbox("First Line", indicatorList)
                    with column2:
                        secondLine = st.selectbox("Second Line", indicatorList)
                if selectedStrategy == "Boundary":
                    column1, column2, column3 = st.columns([0.75, 1.5, 0.75])
                    with column1:
                        lowerBoundary = st.number_input("Lower Boundary", value=0.2)
                    with column2:
                        line = st.selectbox("indicator", indicatorList)
                    with column3:
                        upperBoundary = st.number_input("Upper Boundary", value=0.8)
                if st.button("Add Strategy"):
                    if selectedStrategy == "Cross Over":
                        st.session_state.strategy.useCrossOver(firstLine=firstLine, secondLine=secondLine)
                    if selectedStrategy == "Boundary":
                        st.session_state.strategy.useUpperLowerBoundary(line=line, upperBoundary=upperBoundary, lowerBoundary=lowerBoundary)
            
            with st.container(border=True):
                st.write(st.session_state.strategy.getStrategyList())

        with graphTab:
            indicatorList = st.session_state.indicator.getIndicatorList()
            options = st.multiselect(
                "Show Indicator(s)",
                indicatorList
            )

            mainChart = go.Figure(data=[go.Candlestick(
                x=st.session_state.data.index,
                open=st.session_state.data['Open'],
                high=st.session_state.data['High'],
                low=st.session_state.data['Low'],
                close=st.session_state.data['Close'],
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
                elif "RSI" in indicatorName or "Stoch" in indicatorName:
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
                xaxis_title='Date',
                yaxis_title='Price',
                xaxis_rangeslider_visible=False,
                height=450,
                margin={
                    "b": 0,
                    "t": 0
                }
            )

            MACDChart.update_layout(
                yaxis_title='MACD',
                xaxis_rangeslider_visible=False,
                height=200,
                margin={
                    "b": 0,
                    "t": 0
                }
            )

            RSIChart.update_layout(
                yaxis_title='RSI/Stoch',
                xaxis_rangeslider_visible=False,
                height=200,
                margin={
                    "b": 0,
                    "t": 0
                }
            )

            with dataTab:
                with dataTab_col3:
                    netValueChart = go.Figure()
                    with st.container(border=True):
                        initialFund = st.number_input("Initial Fund", value=100000)
                        stockAmountBuy = st.number_input("Number of stock per position", value=100)
                        if st.button("Run Test", type="primary"):
                            backtestr = Backtestr(st.session_state.data, ticker_symbol)
                            st.session_state.backtestr = backtestr

                            netValue = st.session_state.backtestr.runTest(initialFund, stockAmountBuy)
                            st.write(netValue)

                            buy_signals = st.session_state.data[st.session_state.data['Buy'] == True]
                            sell_signals = st.session_state.data[st.session_state.data['Sell'] == True]

                            mainChart.add_trace(go.Scatter(
                                x=buy_signals.index,
                                y=buy_signals['Low']*97/100,  # Place markers just below the low price
                                mode='markers',
                                marker=dict(symbol='triangle-up', color='green', size=10),
                                name='Buy'
                            ))
                            mainChart.add_trace(go.Scatter(
                                x=sell_signals.index,
                                y=sell_signals['High']*103/100,  # Place markers just below the low price
                                mode='markers',
                                marker=dict(symbol='triangle-down', color='red', size=10),
                                name='Sell'
                            ))

                            netValueChart.add_trace(go.Scatter(
                                                x=st.session_state.data.index,
                                                y=st.session_state.data.netValue,
                                                mode='lines',
                                                name='Net Value'
                                            ))
                            netValueChart.update_layout(
                                yaxis_title='Net Value',
                                xaxis_rangeslider_visible=False,
                                height=250,
                                margin={
                                    "b": 0,
                                    "t": 0
                                }
                            )
                        st.write(netValueChart)
            with st.container(border=True):
                st.write(mainChart)
            with st.container(border=True):
                st.write(MACDChart)
            with st.container(border=True):
                st.write(RSIChart)



with featureRequestTab:
    with st.container():
        st.markdown("""
            <style>
            .stApp {
                max-width: 800px;
                margin: auto;
                padding: 2rem;
            }
            </style>
            """, unsafe_allow_html=True)
        with st.form(key='feature_request_form'):
            # Collect user inputs
            name = st.text_input('Name')
            email = st.text_input('Email')
            
            # Type of request with checkboxes
            st.subheader('Type of Request')
            new_feature = st.checkbox('New Feature')
            improvement = st.checkbox('Improvement')
            bug_report = st.checkbox('Bug Report')
            other = st.checkbox('Other')
            other_text = st.text_input('If other, please specify:')
            
            # Description
            description = st.text_area('Description')

            # Submit button
            submit_button = st.form_submit_button(label='Submit', type="primary")

            if submit_button:
                if not (name and email and (new_feature or improvement or bug_report or (other and other_text)) and description):
                    st.error('All fields are required.')
                else:
                    st.success('Feature request submitted successfully!')

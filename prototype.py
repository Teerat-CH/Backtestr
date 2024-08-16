from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(layout="wide")

st.title("Backtestr")

dataTab, graphTab, searchTab, docTab, featureRequestTab = st.tabs(["🗃 Data", "📈 Chart", "🔎 Stock Search", "📄 Documentation", "💡 Feature Request"])

with dataTab:
    dataTab_col1, dataTab_col2, dataTab_col3 = st.columns([1, 1, 1])
    with dataTab_col1:
        st.write("##### 1. Select and Download Stock Data")
        with st.container(border=True):
            stockCol, periodCol, intervalCol, downloadCol = st.columns([2, 1.5, 1.5, 1])
            with stockCol:
                stockName = st.selectbox("Stock", ("---", "BTC-USD", "ADVANC", "AOT", "AWC", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC", "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"))
            with periodCol:
                period = st.selectbox("Period", ("---", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"))
            with intervalCol:    
                interval = st.selectbox("Interval", ("---", "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo"))
            with downloadCol:
                st.write("######")
                downloadButton = st.button(" 📥 ")

        if stockName != "---" and period != "---" and interval != "---":
            if stockName != "BTC-USD":
                ticker_symbol = stockName + ".bk"
            else:
                ticker_symbol = stockName
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

            st.write("##### 2. Add indicator(s)")
            st.write("- Added indicator(s) can be plotted in the Chart Tab")
            with st.container(border=True):
                selectedIndicator = st.selectbox("Select Indicator", ("---", "MA", "EMA", "MACD", "RSI", "StochRSI", "StochOscillator", "LinearLine"), key="input_indicator")
                if selectedIndicator in ["MA", "EMA", "RSI", "StochRSI", "StochOscillator"]:
                    averageInterval = st.slider("Average Interval", min_value=0, max_value=100, step=1, value=20)
                if selectedIndicator in ["MACD"]:
                    firstAverageInterval = st.slider("First Average Interval", min_value=1, max_value=100, step=1, value=12)
                    secondAverageInterval = st.slider("Second Average Interval", min_value=1, max_value=100, step=1, value=26)
                    signalAverageInterval = st.slider("Signal Average Interval", min_value=1, max_value=100, step=1, value=9)
                if selectedIndicator in ["LinearLine"]:
                    value = st.slider("Value", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
                    
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
                    if selectedIndicator == "LinearLine":
                        st.session_state.indicator.makeLinearLine(value)
            
                st.write(st.session_state.indicator)

            st.write("##### 3. Add Buy and Sell Strategy")
            with st.container(border=True):
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

                andOr = st.toggle("And/Or", value=False)
                if andOr:
                    st.write(f"Use **AND**")
                else:
                    st.write(f"Use **OR**")

                if st.button("Add Buy Strategy"):
                    if selectedStrategy == "Cross Over":
                        st.session_state.strategy.useCrossOver(action="buy", logic=andOr, firstLine=firstLine, secondLine=secondLine)
                    if selectedStrategy == "Boundary":
                        st.session_state.strategy.useUpperLowerBoundary(action="buy", logic=andOr, line=line, upperBoundary=upperBoundary, lowerBoundary=lowerBoundary)

                if st.button("Add Sell Strategy"):
                    if selectedStrategy == "Cross Over":
                        st.session_state.strategy.useCrossOver(action="sell", logic=andOr, firstLine=firstLine, secondLine=secondLine)
                    if selectedStrategy == "Boundary":
                        st.session_state.strategy.useUpperLowerBoundary(action="sell", logic=andOr, line=line, upperBoundary=upperBoundary, lowerBoundary=lowerBoundary)

                if st.button("Clear Strategy"):
                    st.session_state.strategy.clearStrategy()
                    
                st.write(st.session_state.strategy.getStrategyList())

        with graphTab:
            indicatorList = st.session_state.indicator.getIndicatorList()
            options = st.multiselect(
                "##### Show Indicator(s)",
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
                elif "LinearLine" in indicatorName:
                    RSIChart.add_trace(go.Scatter(
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
                    st.write("##### 4. Run the Back Test!")
                    netValueChart = go.Figure()
                    netValueChart.update_layout(
                                yaxis_title='Net Value',
                                xaxis_rangeslider_visible=False,
                                height=250,
                                margin={
                                    "b": 0,
                                    "t": 0
                                }
                            )
                    with st.container(border=True):
                        initialFund = st.number_input("Initial Fund", value=100000)
                        stockAmountBuy = st.number_input("Number of stock per position Buy", value=100)
                        stockAmountSell = st.number_input("Number of stock per position Sell", value=100)
                        if st.button("Run Test", type="primary"):
                            backtestr = Backtestr(st.session_state.data, ticker_symbol)
                            st.session_state.backtestr = backtestr

                            netValue = st.session_state.backtestr.runTest(initialFund, stockAmountBuy, stockAmountSell)
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
                        st.write(netValueChart)
            with st.container(border=True):
                st.write(mainChart)
            with st.container(border=True):
                st.write(MACDChart)
            with st.container(border=True):
                st.write(RSIChart)

with searchTab:
    stockList = []
    searchOption = st.selectbox("Search From", ["SET50"])
    period = st.selectbox("Period", ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"))
    interval = st.selectbox("Interval", ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo"))

    SET50 = ["ADVANC", "AOT", "AWC", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC", "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"]
    
    import time

    progress_text = "Operation in progress. Please wait."
    if st.button("Search"):
        my_bar = st.progress(0, text=progress_text)
        i = 0
        step = int(100/len(SET50))
        for stock in SET50:
            i+=step
            time.sleep(0.01)
            my_bar.progress(i, text=progress_text)
            if stock != "---":
                ticker_symbol = stock + ".bk"
                stockTicker = yf.Ticker(ticker_symbol)
                data = stockTicker.history(period=period, interval=interval).reset_index(drop=True)
                stockList.append(stock)
        st.write(stockList)
        if i >= 100:
            my_bar.progress(i, text="Search Completed")


with featureRequestTab:
    featureRequestTab_col1, featureRequestTab_col2, featureRequestTab_col3 = st.columns([1,1,1])
    with featureRequestTab_col2:
        with st.form(key='feature_request_form'):
            st.subheader('Feature Request Form')
            # Collect user inputs
            name = st.text_input('Name')
            email = st.text_input('Email')
        
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

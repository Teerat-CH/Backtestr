from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import streamlit_nested_layout
import smtplib
from email.mime.text import MIMEText

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
                selectIndicatorCol, addIndicatorCol = st.columns([5,1])
                with selectIndicatorCol:
                    selectedIndicator = st.selectbox("Select Indicator", ("---", "MA", "EMA", "MACD", "RSI", "StochRSI", "StochOscillator", "RSILinearLine", "MACDLinearLine"), key="input_indicator")
                if selectedIndicator in ["MA", "EMA", "RSI", "StochRSI", "StochOscillator"]:
                    averageInterval = st.slider("Average Interval", min_value=0, max_value=100, step=1, value=20)
                if selectedIndicator in ["MACD"]:
                    firstAverageInterval = st.slider("First Average Interval", min_value=1, max_value=100, step=1, value=12)
                    secondAverageInterval = st.slider("Second Average Interval", min_value=1, max_value=100, step=1, value=26)
                    signalAverageInterval = st.slider("Signal Average Interval", min_value=1, max_value=100, step=1, value=9)
                if "LinearLine" in selectedIndicator:
                    value = st.slider("Value", min_value=-1.0, max_value=1.0, step=0.01, value=0.0)
                
                with addIndicatorCol:
                    st.write("######")
                    if st.button("Add"):
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
                        if selectedIndicator == "RSILinearLine":
                            st.session_state.indicator.makeRSILinearLine(value)
                        if selectedIndicator == "MACDLinearLine":
                            st.session_state.indicator.makeMACDLinearLine(value)
            
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

                andOrCol, terminateCol, spaceCol_toggle = st.columns([1, 1, 2])

                with andOrCol:
                    andOr = st.toggle("And/Or", value=False)

                    if andOr:
                        st.write(f"Use **AND**")
                    else:
                        st.write(f"Use **OR**")

                with terminateCol:
                    terminate = st.toggle("Terminate", value = False)
                    st.write("Terminate = " + "**" + str(terminate) + "**")

                addBuyStrategyCol, addSellStrategyCol, clearStrategyCol, spaceCol = st.columns([1, 1, 1, 0.5])

                with addBuyStrategyCol:
                    if st.button("Add Buy Strategy"):
                        if selectedStrategy == "Cross Over":
                            st.session_state.strategy.useCrossOver(action="buy", logic=andOr, terminate=terminate, firstLine=firstLine, secondLine=secondLine)
                        if selectedStrategy == "Boundary":
                            st.session_state.strategy.useUpperLowerBoundary(action="buy", logic=andOr, terminate=terminate, line=line, upperBoundary=upperBoundary, lowerBoundary=lowerBoundary)

                with addSellStrategyCol:
                    if st.button("Add Sell Strategy"):
                        if selectedStrategy == "Cross Over":
                            st.session_state.strategy.useCrossOver(action="sell", logic=andOr, terminate=terminate, firstLine=firstLine, secondLine=secondLine)
                        if selectedStrategy == "Boundary":
                            st.session_state.strategy.useUpperLowerBoundary(action="sell", logic=andOr, terminate=terminate, line=line, upperBoundary=upperBoundary, lowerBoundary=lowerBoundary)

                with clearStrategyCol:
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
                elif "RSILinearLine" in indicatorName:
                    RSIChart.add_trace(go.Scatter(
                        x=st.session_state.data.index,
                        y=st.session_state.data[indicatorName],
                        mode='lines',
                        name=indicatorName
                    ))
                elif "MACDLinearLine" in indicatorName:
                    MACDChart.add_trace(go.Scatter(
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

                        usePercentBuy = False
                        usePercentSell = False
                        stockAmountBuyCol, stockAmountSellCol, runTestCol = st.columns([3, 3, 1])
                        with stockAmountBuyCol:
                            stockAmountBuy = st.number_input("Number of stock per position Buy", value=100.0)
                        with stockAmountSellCol:
                            stockAmountSell = st.number_input("Number of stock per position Sell", value=100.0)
                        minimumStockPerPosition = 0

                        with runTestCol:
                            st.write("######")
                            if st.button("Run", type="primary"):
                                backtestr = Backtestr(st.session_state.data, ticker_symbol)
                                st.session_state.backtestr = backtestr

                                netValue = st.session_state.backtestr.runTest(initialFund=initialFund, usePercentBuy=usePercentBuy, stockAmountBuy=stockAmountBuy, usePercentSell=usePercentSell, stockAmountSell=stockAmountSell, minimumStockPerPosition=minimumStockPerPosition)
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
    st.header("Coming Soon!")
    st.write("- Stock search will allow you to search for a stock that meet your condition(s). For example, searching for a stock whose MACD just cross over or RSI is oversold will be possible.")
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
    featureRequestTab_col1, featureRequestTab_col2, featureRequestTab_col3, featureRequestTab_col4 = st.columns([1,1,1,1])

    with featureRequestTab_col2:
        pass

    with featureRequestTab_col3:
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

            email_sender = 'teerat.backtestr@gmail.com'
            email_receiver = 'teerat.backtestr@gmail.com'

            subject = "Backtestr -"

            if new_feature:
                subject += " New Feature,"
            if improvement:
                subject += " Improvement,"
            if bug_report:
                subject += " Bug Report,"
            if other:
                subject += " Other: " + other_text

            body = "From " + name + "\n" + email + "\n\n"
            body += description

            if submit_button:
                if not (name and email and (new_feature or improvement or bug_report or (other and other_text)) and description):
                    st.error('All fields are required.')
                else:
                    try:
                        with st.spinner("Submitting the form"):
                            msg = MIMEText(body)
                            msg['From'] = email_sender
                            msg['To'] = email_receiver
                            msg['Subject'] = subject

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(st.secrets["email"]["gmail"], st.secrets["email"]["password"])
                            server.sendmail(email_sender, email_receiver, msg.as_string())
                            server.quit()

                        st.success('Form submitted successfully! 🚀')
                    except Exception as e:
                        st.error("Failed to submit the form")
                

with docTab:
    st.write("### Portfolio")
    with st.expander("- **Initialize Portfolio**"):
        st.code('''Portfolio = Portfolio(data) # let data be dataframe containing Open, Close, High, and Low values''')
    with st.expander("- **Set buy position**"):
        st.code('''Portfolio.buy(stockName: str, stockAmount: int, stockPrice: float)''')
        st.markdown("""
                    * **Input**
                        * :red[stockName]: The name of the stock
                        * :red[stockAmount]: the number of stock to buy in this position
                        * :red[stockPrice]: The price of stock to buy at your position
                    * **Output**
                        * :red[Boolean]: :blue[True] if the order is valid and :blue[False] otherwise
                    """)
    with st.expander("- **Set sell position**"):
        st.code('''Portfolio.sell(stockName: str, stockAmount: int, stockPrice: float)''')
        st.markdown("""
                    * **Input**
                        * :red[stockName]: The name of the stock
                        * :red[stockAmount]: the number of stock to sell in this position
                        * :red[stockPrice]: The price of stock to sell at your position
                    * **Output**
                        * :red[Boolean]: :blue[True] if the order is valid and :blue[False] otherwise
                    """)
    with st.expander("- **Get the amount of cash in the portfolio**"):
        st.code('''Portfolio.getCash()''')
        st.markdown("""
                    * **Input**
                        * :blue[None]
                    * **Output**
                        * :red[Float]: Total cash left in the portfolio
                    """)
    with st.expander("- **Add Fund**"):
        st.code('''Portfolio.addFund(fund: float)''')
    with st.expander("- **Sell all current stock**"):
        st.code('''Portfolio.cashOut(cashAmout: float)''')
    with st.expander("- **Get number of specific stock in the portfolio**"):
        st.code('''Portfolio.getStockAmount(stockName: str)''')
    with st.expander("- **Get the valud of all stock in the portfolio**"):
        st.code('''Portfolio.getStockValue()''')
    with st.expander("- **Get portfolio net value**"):
        st.code('''Portfolio.getNetValue()''')
    with st.expander("- **Get current set fee**"):
        st.code('''Portfolio.getFee()''')
    with st.expander("- **Set current fee**"):
        st.code('''Portfolio.setFee()''')
    with st.expander("- **Add audit log**"):
        st.code('''Portfolio.addLog(action: str, stockName: str, amount: int, price: float, date: object)''')
    with st.expander("- **Get all audit log**"):
        st.code('''Portfolio.getLog()''')
    with st.expander("- **Get number of each stocks in the portfolio**"):
        st.code('''Portfolio.getStockDirectory()''')
    with st.expander("- **Show portfolio details**"):
        st.code('''print(portfolio)''')
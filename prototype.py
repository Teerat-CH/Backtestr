from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import pandas as pd
import streamlit as st
import yfinance as yf

# data = yf.download()

# Backtestr = Backtestr(data)
# Indicator = Indicator(data)
# Strategy = Strategy(data)

# # test for macd cross over strategy with config (12, 26, 9)

# MACDLine, SignalLine = Indicator.makeMACD(firstAverageInterval=12, secondAverageInterval=26, signalAverageInterval=9)
# Strategy.useCrossOver(MACDLine, SignalLine)
# Backtestr.runTest()

st.header("Backtestr Prototype")
stockName = st.selectbox("Select Stock", ("---", "ADVANC", "AOT", "AWC", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC", "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"))

if 'data' not in st.session_state:
    data = pd.DataFrame({'Expense':[],'Amount':[],'Budget':[],'Variance':[]})
    st.session_state.data = data

# show current data (will be empty to first time the page is opened, but will then show the
# incrementally built table of data with each user interactions
st.dataframe(st.session_state.data)

# this is the function the sends the information to that dataframe when called
# variance is calculated at this point
def add_dfForm():
    row = pd.DataFrame({'Expense':[st.session_state.input_indicator],
            'Amount':[st.session_state.input_amount],
            'Budget':[st.session_state.input_budget],
            'Variance':[st.session_state.input_budget-st.session_state.input_amount]})
    st.session_state.data = pd.concat([st.session_state.data, row])

# here's the place for the user to specify information
Form = st.form(clear_on_submit=True, key='dfForm')
with Form:
    dfColumns = st.columns(4)
    with dfColumns[0]:
        indicator = st.selectbox("Select Indicator", ("---", "MA", "EMA", "MACD", "RSI", "StochRSI"), key='input_indicator')
        if indicator == "MA":
            st.write("MA is selected")
    with dfColumns[1]:
        st.number_input('Amount', key='input_amount')
    with dfColumns[2]:
        st.number_input('Budget', key='input_budget')
    with dfColumns[3]:
        st.form_submit_button(on_click=add_dfForm)


st.write({
    "MA": "ma1, ma2",
    "EMA": "ema1, ema2"
})
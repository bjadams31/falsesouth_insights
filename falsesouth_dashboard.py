import numpy as np
import pandas as pd 
import streamlit as st 

########## Set Page Config Parameters ##########
st.set_page_config(
     page_title="FalseNorth Insights",
     layout="wide",
     initial_sidebar_state="expanded",)

########## Data Management ##########
invoice_df = pd.read_excel('./data/falsesouth_receivables.xlsx')

########## Sidebar ##########
st.sidebar.image('./data/img/logo.png', width=300)

st.sidebar.markdown("----")

st.sidebar.markdown('<b><p style="font-size: 29px; text-align: center; color:#d3755c;">Broker Selections</p></b>', unsafe_allow_html=True)


########## Header ##########
st.markdown('<b><p style="font-size: 65px; text-align: center; color:#1d9385;">FalseSouth - Receivables Insights</p></b>', unsafe_allow_html=True)


########## Body ##########

# Top Level Quotes and Summary
st.markdown('<b><p style="font-size: 30px; text-align: left; color:#1d9385;">Invoice Data</p></b>', unsafe_allow_html=True)

st.dataframe(invoice_df.sample(8))
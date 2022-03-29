import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st 

########## Set Page Config Parameters ##########
st.set_page_config(
     page_title="FalseNorth Insights",
     layout="wide",
     initial_sidebar_state="expanded",)

pd.options.display.float_format = "{:,.2f}".format

########## Data Management ##########
invoice_df = pd.read_excel('./data/falsesouth_receivables.xlsx')
invoice_df['LOAD_NUM'] = invoice_df['LOAD_NUM'].astype(str)



########## Header ##########
st.markdown('<b><p style="font-size: 65px; text-align: center; color:#1d9385;">FalseSouth - Receivables Insights</p></b>', unsafe_allow_html=True)

st.text('')
st.text('')

########## Functions ##########

# Function to get total invoiced
def get_total_invoiced(df):
    total_invoiced = df['TOTAL_AMOUNT'].sum()
    return total_invoiced

# Function to get total outstanding
def get_total_outstanding(df):
    total_outstanding = df['BALANCE'].sum()
    return total_outstanding

def get_overdue_invoices(df):
    overdue_df = df[['COMPANY_NAME', 'INVOICE_ID', 'BALANCE']][df['BALANCE'] > 0]
    overdue_df = overdue_df.sort_values(by='BALANCE', ascending=False)
    return overdue_df

def get_monthly_totals(df):
    monthly_df = df.copy()
    monthly_df['INVOICE_DATE'] = pd.to_datetime(monthly_df['INVOICE_DATE'])
    monthly_df = monthly_df[['INVOICE_DATE', 'BALANCE', 'TOTAL_AMOUNT']].set_index('INVOICE_DATE').resample('BMS').sum()
    monthly_df['COLLECTED'] = monthly_df['TOTAL_AMOUNT'] - monthly_df['BALANCE']
    return monthly_df

def get_overdue_counts(df):
    overdue_counts_df = pd.DataFrame(df['COMPANY_NAME'][df['BALANCE'] > 0].value_counts()
        ).reset_index().rename(columns={'index': 'COMPANY_NAME', 'COMPANY_NAME': 'OVERDUE_COUNTS'}).sort_values(by='OVERDUE_COUNTS', ascending=False)
    return overdue_counts_df

########## Body ##########

total_invoiced = get_total_invoiced(invoice_df)
total_outstanding = get_total_outstanding(invoice_df)

# st.markdown('<b><p style="font-size: 45px; text-align: center; color:#d3755c;">Collection Effort Metrics</p></b>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("Total Invoiced", "${:,.2f}".format(total_invoiced))
col2.metric("Total Collected", "${:,.2f}".format(total_invoiced - total_outstanding))
col3.metric("Total Outstanding", "${:,.2f}".format(total_outstanding))

st.text('')
st.text('')

monthly_totals = get_monthly_totals(invoice_df)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bar plot trace for monthly COLLECTED
fig.add_trace(
    go.Bar(x=monthly_totals.index, y=monthly_totals['COLLECTED'], name="Monthly Collected Totals"))
 
# Add bar plot trace for monthly UNCOLLECTED
fig.add_trace(
    go.Bar(x=monthly_totals.index, y=monthly_totals['BALANCE'], name="Monthly Uncollected Totals"))
 
# Add title, plot size, theme
fig.update_layout(
    title_text="Monthly Invoice Totals - Collected vs. Uncollected",
    height = 550,
    width = 1600,
    template = 'seaborn',
    barmode='stack',
    legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=18,
            color="black"
        ),
    )
)
st.plotly_chart(fig)

st.text('')
st.text('')

col1, col2 = st.columns(2)

overdue_brokers = get_overdue_invoices(invoice_df)
overdue_counts = get_overdue_counts(invoice_df)

col1.markdown('<b><p style="font-size: 29px;  color:#d3755c;">Collection Priorities</p></b>', unsafe_allow_html=True)
col1.dataframe(overdue_brokers.style.hide_index())
col2.markdown('<b><p style="font-size: 29px;  color:#d3755c;">High Risk Brokers</p></b>', unsafe_allow_html=True)
col2.dataframe(overdue_counts)



import streamlit as st
from snowflake.snowpark.session import Session
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Financial Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

connection_parameters = {
    "account": "pr23558.central-india.azure",
    "user": "ROHITGOSWAMI",
    "password": "Lonewolf@853@",
    "warehouse": "COMPUTE_WH",
    "database": "Stock_json",
    "schema": "PUBLIC"
}
session = Session.builder.configs(connection_parameters).create()

def get_data(sql):
    return session.sql(sql).to_pandas()

session = Session.builder.configs(connection_parameters).create()

def get_data(sql):
    return session.sql(sql).to_pandas()

st.title("Snowflake Tables in stock_json Database")

sql_query_tables = """
    SELECT Filename FROM Stock_Table;
"""
filenames_df = get_data(sql_query_tables)

st.write(f"There are {len(filenames_df)} filenames in the Stock_Table:")

filename_list = filenames_df['FILENAME'].tolist()
selected_filename = st.selectbox("Select a filename to view its contents:", filename_list)

if selected_filename:
    sql_add1 = f"""
        SELECT Address1
        FROM assetprofile
        WHERE Filename = '{selected_filename}';
    """
    st.write("Details: ")

    add1 = get_data(sql_add1)
    for address in add1['ADDRESS1']:
        st.write(f"Address1:{address}")

    sql_add2 = f"""
        SELECT Address2
        FROM assetprofile
        WHERE Filename = '{selected_filename}';
    """ 
    add2 = get_data(sql_add2)
    for address in add2['ADDRESS2']:
        st.write(F"Address2:{address}")
    
    sql_INDUSTRY = f"""
        SELECT INDUSTRY
        FROM assetprofile
        WHERE Filename = '{selected_filename}';
    """   
    INDUSTRY = get_data(sql_INDUSTRY)
    st.dataframe(INDUSTRY)
    
    sql_WEBSITE = f"""
        SELECT WEBSITE
        FROM assetprofile
        WHERE Filename = '{selected_filename}';
    """   
    WEBSITE = get_data(sql_WEBSITE)
    for i in WEBSITE['WEBSITE']:
        st.write(F"WEBSITE:{i}")

    sql_balancesheet = f"""
        SELECT *
        FROM balanceSheetHistory
        WHERE Filename = '{selected_filename}';
    """  
    balanceSheet = get_data(sql_balancesheet)
    st.dataframe(balanceSheet)

    sql_keyStats = f"""
        SELECT *
        FROM defaultKeyStatistics
        WHERE Filename = '{selected_filename}';
    """  
    keyStats = get_data(sql_keyStats)
    st.dataframe(keyStats)

    sql_financialData = f"""
        SELECT *
        FROM financialData
        WHERE Filename = '{selected_filename}';
    """  
    financialData = get_data(sql_financialData)
    st.dataframe(financialData)

    sql_priceDetails = f"""
        SELECT *
        FROM financialData
        WHERE Filename = '{selected_filename}';
    """  
    priceDetails = get_data(sql_priceDetails)
    st.dataframe(priceDetails)

    sql_query_data = f"""
        SELECT *
        FROM cashflowStatementHistory
        WHERE Filename = '{selected_filename}';
    """
    data_df = get_data(sql_query_data)

    st.subheader("Bar Chart Analysis")
    bar_chart_columns = [
        'CAPITALEXPENDITURES', 'CHANGEINCASH', 'CHANGETOACCOUNTRECEIVABLES', 
        'CHANGETOINVENTORY', 'CHANGETOLIABILITIES', 'CHANGETONETINCOME',
        'CHANGETOOPERATINGACTIVITIES', 'DEPRECIATION', 'INVESTMENTS',
        'NETBORROWINGS', 'NETINCOME', 'OTHERCASHFLOWSFROMFINANCINGACTIVITIES',
        'OTHERCASHFLOWSFROMINVESTINGACTIVITIES', 'TOTALCASHFROMFINANCINGACTIVITIES',
        'TOTALCASHFROMOPERATINGACTIVITIES', 'TOTALCASHFLOWSFROMINVESTINGACTIVITIES'
    ]
    bar_chart_column = st.selectbox("Select a column for bar chart analysis:", bar_chart_columns)
    fig = px.bar(data_df, x='ENDDATE', y=bar_chart_column, title=f"{bar_chart_column} of {selected_filename}")
    st.plotly_chart(fig)

    sql_insiderHolders = f"""
    SELECT *
    FROM insiderHolders
    WHERE Filename = '{selected_filename}' and POSITIONDIRECT is not null;
"""
    insiderHolders = get_data(sql_insiderHolders)
    insiderHolders['LATESTTRANSDATE_NAME'] = insiderHolders['LATESTTRANSDATE'].astype(str) + " - " + insiderHolders['NAME']
    fig = px.bar(insiderHolders, x='LATESTTRANSDATE_NAME', y='POSITIONDIRECT', title="Bar Chart of Latest Transactions")
    st.plotly_chart(fig)

session.close()


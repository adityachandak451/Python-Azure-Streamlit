import streamlit as st
from snowflake.snowpark.session import Session
import pandas as pd

# Initialize Snowflake session
connection_parameters = {
    "account": "lh****india.azure",
    "user": "abc",
    "password": "abc@10",
    "warehouse": "COMPUTE_WH",
    "database": "JSON_DB",
    "schema": "PUBLIC"
}
session = Session.builder.configs(connection_parameters).create()

# Set Streamlit title
st.title("Cricket Match Data")

# Define helper function to retrieve data
def get_data(sql):
    return session.sql(sql).to_pandas()

# Retrieve distinct years
sql_years = "SELECT DISTINCT YEAR(dates) AS year FROM json_db.public.T20_EVENT ORDER BY year"
years_data = get_data(sql_years)

# Display year filter
year_option = st.selectbox("Choose YEAR", years_data['YEAR'])

# Retrieve events based on selected year
sql_events = f"SELECT DISTINCT name FROM json_db.public.T20_EVENT WHERE YEAR(dates) = {year_option}"
events_data = get_data(sql_events)

# Display event filter
event_option = st.selectbox("Choose Event", events_data['NAME'])

# Filter and display table
if st.button("Show Filtered Table"):
    sql_filtered_table = f"""
    SELECT * FROM json_db.public.T20_EVENT
    WHERE YEAR(dates) = {year_option} AND name = '{event_option}'
    """
    filtered_table_data = get_data(sql_filtered_table)
    st.write(filtered_table_data)

# Display full table
if st.button("Show Full Table"):
    sql_full_table = "SELECT * FROM json_db.public.T20_EVENT"
    full_table_data = get_data(sql_full_table)
    st.write(full_table_data)


# Retrieve and select teams
sql = f"""
SELECT id, team1, team2 
FROM json_db.public.T20_EVENT
WHERE id IN (
    SELECT id 
    FROM json_db.public.T20_EVENT
    WHERE name ='{event_option}' 
    AND year(to_date(dates))='{year_option}'
)
"""
teams_data = get_data(sql)
col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox('TEAM1', teams_data.TEAM1.unique())
with col2:
    team2 = st.selectbox('TEAM2', teams_data.TEAM2.unique())

# Filter match data
match = teams_data[teams_data['TEAM1'].isin([team1]) & teams_data['TEAM2'].isin([team2])]
if match.empty:
    st.write("No data")
else:
    match_id = match['ID'].to_list()[0]
    
    # # Display match result
    # sql = f"SELECT result_by FROM json_db.public.Innings WHERE id={match_id}"
    # result_data = get_data(sql)
    # result = result_data['RESULT_BY'].to_list()[0]
    # color(result)

    # Retrieve and display toss information
    sql = f"SELECT WINNER, DECISION FROM json_db.public.T20_EVENT WHERE ID={match_id}"
    toss_data = get_data(sql)
    toss_winner = toss_data['WINNER'].to_list()[0]
    toss_decision = toss_data['DECISION'].to_list()[0]
    toss_info = f'Toss: {toss_winner}, elected to {toss_decision} first'
    st.write(f':blue[{toss_info}]')

    

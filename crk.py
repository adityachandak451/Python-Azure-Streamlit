import streamlit as st
from snowflake.snowpark.session import Session
import pandas as pd

# Initialize Snowflake session
connection_parameters = {
    "account": "lh81346.central-india.azure",
    "user": "SUBHRADYUTI",
    "password": "Subhra@3010",
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

    # # Adjust and display innings information
    # if toss_decision == 'bat' and team2 == toss_winner:
    #     team1, team2 = team2, team1
    # elif toss_decision != 'bat' and team1 == toss_winner:
    #     team1, team2 = team2, team1

    # # Retrieve and display Team1 batting scorecard
    # sql = f"""
    # SELECT BATTER, 
    #        CASE WHEN STATUS IS NULL THEN 'Not Out' ELSE STATUS END AS STATUS, 
    #        RUNS::string RUNS, 
    #        BOWL, 
    #        "4s", 
    #        "6s", 
    #        SR 
    # FROM json_db.public.Innings 
    # WHERE id={match_id} AND TEAM='{team1}' 
    # ORDER BY BATTER_ORDER
    # """
    # team1_batting_data = get_data(sql)
    # st.dataframe(team1_batting_data, hide_index=True)

#     # Retrieve and display Team1 extras and bowling scorecard
#     sql = f"SELECT EXTRAS FROM VW_T20_EXTRAS WHERE id={match_id} AND TEAM='{team1}'"
#     extras_data = get_data(sql)
#     extras = extras_data['EXTRAS'].to_list()[0]
#     col1, _, col2 = st.columns(3)
#     with col1:
#         st.write('Extras')
#     with col2:
#         st.write(extras)

#     sql = f"""
#     SELECT BOWLER, 
#            OVERS, 
#            RUNS::string RUNS, 
#            NVL(WD,0)::string WD, 
#            NVL(NB,0)::string NB, 
#            W 
#     FROM VW_T20_DELIVERIES_BOWLING_SCORE 
#     WHERE id={match_id} AND TEAM='{team1}'
#     """
#     team1_bowling_data = get_data(sql)
#     st.dataframe(team1_bowling_data, hide_index=True)

#     # Retrieve and display Team1 additional details (Did Not Bat, Fall of Wickets)
#     sql = f"SELECT PLAYER_LIST FROM VW_PLAYET_YET_BAT WHERE id={match_id} AND TEAM='{team1}'"
#     did_not_bat_data = get_data(sql)
#     if did_not_bat_data['PLAYER_LIST'].to_list():
#         st.write('Did not Bat yet')
#         st.write(did_not_bat_data['PLAYER_LIST'].to_list()[0])

#     sql = f"SELECT RESULT FROM VW_T20_FALL_WICKETS WHERE id={match_id} AND TEAM='{team1}'"
#     fall_of_wickets_data = get_data(sql)
#     if fall_of_wickets_data['RESULT'].to_list():
#         st.write('Fall of Wickets')
#         st.write(fall_of_wickets_data['RESULT'].to_list()[0])

#     # Repeat for Team2
#     sql = f"SELECT SC_WICKET, OVER_STATUS FROM VW_SCORE_WICKET WHERE id={match_id} AND TEAM='{team2}'"
#     team2_score_data = get_data(sql)
#     team2_score = team2_score_data['SC_WICKET'].to_list()[0] + '(' + team2_score_data['OVER_STATUS'].to_list()[0] + ')'

#     col1, _, col2 = st.columns(3)
#     with col1:
#         st.write(f'{team2} Innings')
#     with col2:
#         st.write(team2_score)

#     sql = f"""
#     SELECT BATTER, 
#            CASE WHEN STATUS IS NULL THEN 'Not Out' ELSE STATUS END AS STATUS, 
#            RUNS::string RUNS, 
#            BOWL, 
#            "4s", 
#            "6s", 
#            SR 
#     FROM json_db.public.Innings
#     WHERE id={match_id} AND TEAM='{team2}' 
#     ORDER BY BATTER_ORDER
#     """
#     team2_batting_data = get_data(sql)
#     st.dataframe(team2_batting_data, hide_index=True)

#     sql = f"SELECT EXTRAS FROM VW_T20_EXTRAS WHERE id={match_id} AND TEAM='{team2}'"
#     team2_extras_data = get_data(sql)
#     team2_extras = team2_extras_data['EXTRAS'].to_list()[0]
#     col1, _, col2 = st.columns(3)
#     with col1:
#         st.write('Extras')
#     with col2:
#         st.write(team2_extras)

#     sql = f"""
#     SELECT BOWLER, 
#            OVERS, 
#            RUNS::string RUNS, 
#            NVL(WD,0)::string WD, 
#            NVL(NB,0)::string NB, 
#            W 
#     FROM VW_T20_DELIVERIES_BOWLING_SCORE 
#     WHERE id={match_id} AND TEAM='{team2}'
#     """
#     team2_bowling_data = get_data(sql)
#     st.dataframe(team2_bowling_data, hide_index=True)

#     sql = f"SELECT PLAYER_LIST FROM VW_PLAYET_YET_BAT WHERE id={match_id} AND TEAM='{team2}'"
#     team2_did_not_bat_data = get_data(sql)
#     if team2_did_not_bat_data['PLAYER_LIST'].to_list():
#         st.write('Did not Bat yet')
#         st.write(team2_did_not_bat_data['PLAYER_LIST'].to_list()[0])

#     sql = f"SELECT RESULT FROM VW_T20_FALL_WICKETS WHERE id={match_id} AND TEAM='{team2}'"
#     team2_fall_of_wickets_data = get_data(sql)
#     if team2_fall_of_wickets_data['RESULT'].to_list():
#         st.write('Fall of Wickets')
#         st.write(team2_fall_of_wickets_data['RESULT'].to_list()[0])

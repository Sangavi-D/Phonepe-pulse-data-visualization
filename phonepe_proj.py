#Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

#Streamlit page setup

st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

st.page_link("phonepe_proj.py", label="Home", icon="🏠")
st.page_link("pages/Facts.py", label="Facts", icon="🎯")

#SQL connection

mydb = mysql.connector.connect(
 host="localhost",
 user="Your username",
 password="Enter your password",
 database = "Enter your database name"


)
print(mydb)
mycursor = mydb.cursor(buffered=True)

#MYSQL TABLE CONVERTED TO DATAFRAMES 
#AGGREGATED_TRANSACTION_DATAFRAME
mycursor.execute("SELECT * FROM AGG_TRANS")
table_rows1 = mycursor.fetchall()
df1 = pd.DataFrame(table_rows1,columns=mycursor.column_names)

#MAP_USERS DATAFRAME
mycursor.execute("SELECT * FROM MAP_USERS")
table_rows4 = mycursor.fetchall()
df4 = pd.DataFrame(table_rows4,columns=mycursor.column_names)

#Function to get the dataframe for a particular year grouped by state and year
  
def transaction(year):
    trans_df = df1[df1["Year"] == year]
    trans_df.reset_index(drop = True,inplace = True)
    trans_grouped_df = trans_df.groupby(['Year', 'State'])[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    return trans_grouped_df

def users(year):
    users_df = df4[df4["Year"] == year]
    users_df.reset_index(drop = True,inplace = True)
    users_grouped_df = users_df.groupby(['Year', 'State'])['Registered_users'].sum().reset_index()
    return users_grouped_df
   
#Streamlit home page   
#Creation of tabs to get Transaction count,amount and registered users across India
tab1, tab2,tab3 = st.tabs(["Transaction count", "Transaction amount","Registered users"])
#Transaction count
with tab1:
   
   years = st.selectbox(
   "Year",
   df1["Year"].unique(),
   index=None,
   placeholder="Select year",
   key="year_selectbox_tab1"
)
  
   st.header( f"TRANSACTION COUNT - {years}")
   fig_count = px.choropleth(
        transaction(years),
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_count',
        color_continuous_scale='tealrose',
        
    )

   fig_count.update_geos(fitbounds="locations", visible=False)
   st.plotly_chart(fig_count, use_container_width=True)
#Transaction amount
with tab2:
   
   years = st.selectbox(
      "Year",
      df1["Year"].unique(),
      index=None,
      placeholder="Select year",
      key="year_selectbox_tab2"
   )
   st.header( f"TRANSACTION AMOUNT - {years}")
   fig_amount = px.choropleth(
        transaction(years),
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_amount',
        color_continuous_scale='tealrose',
        
    )

   fig_amount.update_geos(fitbounds="locations", visible=False)
   
   st.plotly_chart(fig_amount, use_container_width=True)

#Registered users
with tab3:
   
   years = st.selectbox(
      "Year",
      df1["Year"].unique(),
      index=None,
      placeholder="Select year",
      key="year_selectbox_tab3"
   )
   st.header( f"REGISTERED USERS - {years}")
   fig_user = px.choropleth(
        users(years),
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Registered_users',
        color_continuous_scale='tealrose',
        
    )

   fig_user.update_geos(fitbounds="locations", visible=False)
   
   st.plotly_chart(fig_user, use_container_width=True)   





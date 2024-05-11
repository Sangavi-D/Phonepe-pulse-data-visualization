#Import necessary libraries
import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

#MySQL connection

mydb = mysql.connector.connect(
 host="localhost",
 user="Your username",
 password="Enter your password",
 database = "Enter your database name"


)
print(mydb)
mycursor = mydb.cursor(buffered=True)

#Creation of dropdown to view the statistics

option = st.selectbox(
    "Choose to view the chart",
    ('Statewise count of registered users','Device count based on device brands','Top 10 District wise registered users',
     'Percentage of share of current device type compared to all devices for Karnataka','Increase in transaction over the years',
     'App opens over the years','Relation between transaction count and transaction amount','Yearly Trends in Transaction Amounts by Transaction Type',
     'Quarterly Distribution of Transaction Amounts Across Years','Distribution of Transactions Across Types '))

if option == 'Statewise count of registered users':
   mycursor.execute("SELECT State,SUM(Registered_users) AS Registered_users FROM MAP_USERS GROUP BY State")
   table_rowsq1 = mycursor.fetchall()
   dfq1 = pd.DataFrame(table_rowsq1,columns=mycursor.column_names)
   fig1 = px.bar(dfq1,x='State',y='Registered_users',title = 'Statewise count of registered users',color_discrete_sequence = px.colors.sequential.Aggrnyl)
   st.plotly_chart(fig1)
   
if option == 'Device count based on device brands':
   mycursor.execute("SELECT Device_brand,SUM(Device_brand_count) AS Device_count  FROM AGG_USERS GROUP BY Device_brand")
   table_rowsq2 = mycursor.fetchall()
   dfq2 = pd.DataFrame(table_rowsq2,columns=mycursor.column_names)
   fig2 = px.bar(dfq2,x='Device_brand',y='Device_count',title = 'Device count based on device brands',color_discrete_sequence = px.colors.sequential.Viridis)
   st.plotly_chart(fig2)

if option == 'Top 10 District wise registered users':
   mycursor.execute("SELECT District,SUM(Registered_users) AS Registered_users FROM MAP_USERS GROUP BY District ORDER BY Registered_users DESC LIMIT 10")
   table_rowsq3 = mycursor.fetchall()
   dfq3 = pd.DataFrame(table_rowsq3,columns=mycursor.column_names)
   fig3 = px.bar(dfq3,x='District',y='Registered_users',title = 'Top 10 District wise registered users',color_discrete_sequence = px.colors.sequential.haline)
   st.plotly_chart(fig3)

if option == 'Percentage of share of current device type compared to all devices for Karnataka':
   mycursor.execute("SELECT Device_brand,AVG(Device_brand_percent) AS Percentage FROM AGG_USERS WHERE State = 'Karnataka' GROUP BY Device_brand")
   table_rowsq4 = mycursor.fetchall()
   dfq4 = pd.DataFrame(table_rowsq4,columns=mycursor.column_names)  
   fig4 = px.pie(dfq4,values = 'Percentage',names = 'Device_brand',title = 'Percentage of share of current device type compared to all devices for Karnataka',color_discrete_sequence = px.colors.sequential.haline)
   st.plotly_chart(fig4)  

if option == 'Increase in transaction over the years':
   mycursor.execute("SELECT Year,SUM(Transaction_count) AS Transaction_count FROM AGG_TRANS  GROUP BY Year")
   table_rowsq5 = mycursor.fetchall()
   dfq5 = pd.DataFrame(table_rowsq5,columns=mycursor.column_names) 
   fig5 = px.line(dfq5,x = 'Year',y= 'Transaction_count',title = 'Increase in transaction over the years',color_discrete_sequence = px.colors.sequential.Magma,markers=True)
   st.plotly_chart(fig5)           

if option == 'App opens over the years':
   mycursor.execute("SELECT Year,SUM(App_opens) AS App_opens FROM MAP_USERS  GROUP BY Year")
   table_rowsq6 = mycursor.fetchall()
   dfq6 = pd.DataFrame(table_rowsq6,columns=mycursor.column_names) 
   fig6 = px.line(dfq6,x = 'Year',y= 'App_opens',title ='App opens over the years',color_discrete_sequence = px.colors.sequential.Tealgrn,
                  markers=True)
   st.plotly_chart(fig6)  

if option == 'Relation between transaction count and transaction amount':
   mycursor.execute("SELECT SUM(Transaction_count) AS Transaction_count,SUM(Transaction_amount) AS Transaction_amount FROM AGG_TRANS  GROUP BY State")
   table_rowsq7 = mycursor.fetchall()
   dfq7 = pd.DataFrame(table_rowsq7,columns=mycursor.column_names) 
   dfq7 = pd.DataFrame(table_rowsq7,columns=mycursor.column_names) 
   fig7 = px.scatter(dfq7,x = 'Transaction_count',y = 'Transaction_amount', title ='Relation between transaction count and transaction amount',color_discrete_sequence = px.colors.sequential.haline)
   st.plotly_chart(fig7) 

if option == 'Yearly Trends in Transaction Amounts by Transaction Type':
   mycursor.execute("SELECT Year,Transaction_type, Transaction_amount FROM AGG_TRANS GROUP BY Year,Transaction_type ")
   table_rowsq8 = mycursor.fetchall()
   dfq8 = pd.DataFrame(table_rowsq8,columns=mycursor.column_names) 
   fig8 = px.bar(dfq8,x = 'Year',y = 'Transaction_amount',color = 'Transaction_type', title ='Yearly Trends in Transaction Amounts by Transaction Type',color_discrete_sequence = px.colors.sequential.haline)
   st.plotly_chart(fig8)    

if option == 'Quarterly Distribution of Transaction Amounts Across Years':
   mycursor.execute("SELECT Year,Transaction_amount ,Quarter FROM MAP_TRANS GROUP BY Year,Quarter ")
   table_rowsq9 = mycursor.fetchall()
   dfq9 = pd.DataFrame(table_rowsq9,columns=mycursor.column_names) 
   fig9 = px.bar(dfq9,x = 'Year',y ='Transaction_amount',color = 'Quarter', title ='Quarterly Distribution of Transaction Amounts Across Years',color_discrete_sequence = px.colors.sequential.haline)
   st.plotly_chart(fig9)   

if option == 'Distribution of Transactions Across Types ':
   mycursor.execute("SELECT Transaction_type, SUM(Transaction_count) AS Transaction_count FROM AGG_TRANS GROUP BY Transaction_type ")
   table_rowsq10 = mycursor.fetchall()
   dfq10 = pd.DataFrame(table_rowsq10,columns=mycursor.column_names) 
   fig10 = px.pie(dfq10,values = 'Transaction_count',names = 'Transaction_type',title = 'Distribution of Transactions Across Types ',color_discrete_sequence = px.colors.sequential.Electric)
   st.plotly_chart(fig10)  
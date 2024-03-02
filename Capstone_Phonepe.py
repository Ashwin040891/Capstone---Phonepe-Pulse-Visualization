import mysql.connector as sql
import json
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

#CREATE DATAFRAMES FROM SQL
#sql connection
mydb = sql.connect(host="localhost",
                   user="root",
                   password="12345678",
                   database= "phonepe1"
                  )
cursor = mydb.cursor()

#Aggregated Transaction
cursor.execute("select * from agg_trans")
agg_trans = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

#Aggregated User
cursor.execute("select * from agg_user")
agg_user = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "Brand", "User_Count", "Percentage"))

#Map Transaction
cursor.execute("select * from map_trans")
map_trans = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "District", "Transaction_Count", "Transaction_Amount"))

#Map User
cursor.execute("select * from map_user")
map_user = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "District", "User_Count", "App_Opens"))

#Topography Transaction
cursor.execute("select * from top_trans")
top_trans = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "Pincode", "Transaction_Count", "Transaction_Amount"))

#Topography User
cursor.execute("select * from top_user")
top_user = pd.DataFrame(cursor.fetchall(), columns = ("State", "Year", "Quarter", "Pincode", "User_Count"))


def agg_trans_Y(df, year):
    
    dfy = df[df["Year"] == year]
    dfy.reset_index(drop=True, inplace=True)

    #dfyg = dfy.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum()
    #dfyg.reset_index(inplace=True)

    #col1,col2= st.columns(2)
    
    #with col1:
        
    #fig_amount = px.bar(dfyg, x="State", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUNT",
    #                    width=600, height=650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    #st.plotly_chart(fig_amount)
    
    #with col2:
        
    #fig_count = px.bar(dfyg, x="State", y="Transaction_Count", title=f"{year} TRANSACTION COUNT",
    #                   width=600, height=650, color_discrete_sequence=px.colors.sequential.Bluered_r)
    #st.plotly_chart(fig_count)

    #col1,col2= st.columns(2)

    #url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    #response = requests.get(url)
    #data = json.loads(response.content)
    #fc = open(r"C:/Users/Admin/Guvi D102_New/India.geojson")
    #data = json.load(fc)
    #state_names = [feature["properties"]["ST_NM"] for feature in data["features"]]
    #state_names.sort()

    #with col1:

    #fig_india_1= px.choropleth(dfyg,
    #                           geojson = data,
    #                           locations = "State",
    #                           featureidkey = "properties.ST_NM",
    #                           color = "Transaction_Amount",
    #                           color_continuous_scale = "Sunsetdark",
    #                           range_color = (dfyg["Transaction_Amount"].min(), dfyg["Transaction_Amount"].max()),
    #                           hover_name = "State",
    #                           title = f"{year} TRANSACTION AMOUNT",
    #                           fitbounds= "locations",
    #                           width = 900,
    #                           height = 600)
    #fig_india_1.update_geos(visible=False)
    #st.plotly_chart(fig_india_1)

    #with col2:

    #fig_india_2= px.choropleth(dfyg,
    #                           geojson = data,
    #                           locations = "State",
    #                           featureidkey = "properties.ST_NM",
    #                           color = "Transaction_Count",
    #                           color_continuous_scale = "Sunsetdark",
    #                           range_color = (dfyg["Transaction_Count"].min(), dfyg["Transaction_Count"].max()),
    #                           hover_name = "State",
    #                           title = f"{year} TRANSACTION COUNT",
    #                           fitbounds = "locations",
    #                           width = 900,
    #                           height = 600)
    #fig_india_2.update_geos(visible =False)
    #st.plotly_chart(fig_india_2)

    return dfy

def agg_trans_Y_Q(df, quarter):
    
    dfyq = df[df["Quarter"] == quarter]
    dfyq.reset_index(drop= True, inplace= True)

    dfyqg = dfyq.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum()
    dfyqg.reset_index(inplace= True)

    #col1,col2= st.columns(2)

    #with col1:
    #st.write(dfyqg.set_index('State'))    
    fig_q_amount = px.bar(dfyqg, x="State", y="Transaction_Amount", hover_data={'State': True, 'Transaction_Amount': ':,.2f'}, title=f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION AMOUNT",
                          width=900, height=900, color_discrete_sequence=px.colors.sequential.Burg_r)
    #fig_q_amount.update_layout(yaxis_tickformat = ',')
    st.plotly_chart(fig_q_amount)

    #with col2:
        
    fig_q_count = px.bar(dfyqg, x="State", y="Transaction_Count", hover_data={'State': True, 'Transaction_Amount': ':,.2f', 'Transaction_Count': ':,.2f'}, title= f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION COUNT",
                         width=900, height=900, color_discrete_sequence=px.colors.sequential.Cividis_r)
    st.plotly_chart(fig_q_count)

    #col1,col2= st.columns(2)

    #url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    #response = requests.get(url)
    #data = json.loads(response.content)
    fc = open(r"C:/Users/Admin/Guvi D102_New/India.geojson")
    data = json.load(fc)
    state_names = [feature["properties"]["ST_NM"] for feature in data["features"]]
    state_names.sort()

    #with col1:

    fig_india_1 = px.choropleth(dfyqg,
                                geojson = data,
                                locations = "State",
                                featureidkey = "properties.ST_NM",
                                color = "Transaction_Amount",
                                color_continuous_scale = "Sunsetdark",
                                range_color = (dfyqg["Transaction_Amount"].min(),dfyqg["Transaction_Amount"].max()),
                                hover_name = "State",
                                hover_data={'State': True, 'Transaction_Amount': ':,.2f'},
                                title = f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION AMOUNT",
                                fitbounds = "locations",
                                width = 900,
                                height = 600)
    fig_india_1.update_geos(visible =False)
    st.plotly_chart(fig_india_1)
        
    #with col2:

    fig_india_2= px.choropleth(dfyqg,
                               geojson = data,
                               locations = "State",
                               featureidkey = "properties.ST_NM",
                               color = "Transaction_Count",
                               color_continuous_scale = "Sunsetdark",
                               range_color = (dfyqg["Transaction_Count"].min(),dfyqg["Transaction_Count"].max()),
                               hover_name = "State",
                               hover_data={'State': True, 'Transaction_Amount': ':,.2f', 'Transaction_Count': ':,.2f'},
                               title = f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION COUNT",
                               fitbounds = "locations",
                               width = 900,
                               height = 600)
    fig_india_2.update_geos(visible =False)
    st.plotly_chart(fig_india_2)
    
    return dfyq

def agg_trans_type(df, state):
    
    df_state = df[df["State"] == state]
    df_state.reset_index(drop=True, inplace=True)

    aggds = df_state.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    aggds.reset_index(inplace= True)

    fig_hbar_1 = px.bar(aggds, x="Transaction_Count", y="Transaction_Type", orientation="h",
                        hover_data={'Transaction_Type': True, 'Transaction_Count': ':,.2f'},
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width=600, 
                        title=f"{state.upper()} - {year} Q{quarter} - TRANSACTION TYPES AND TRANSACTION COUNT", height= 500)
    #st.plotly_chart(fig_hbar_1)

    fig_hbar_2 = px.bar(aggds, x="Transaction_Amount", y="Transaction_Type", orientation="h",
                        hover_data={'Transaction_Type': True, 'Transaction_Amount': ':,.2f'},
                        color_discrete_sequence=px.colors.sequential.Greens_r, width=600,
                        title=f"{state.upper()} - {year} Q{quarter} - TRANSACTION TYPES AND TRANSACTION AMOUNT", height=500)
    st.plotly_chart(fig_hbar_2)
    st.plotly_chart(fig_hbar_1)
        
def agg_user_plot_1(df, year):
    
    aup1 = df[df["Year"] == year]
    aup1.reset_index(drop= True, inplace= True)
    
    #aup1g = pd.DataFrame(aup1.groupby("Brand")["User_Count"].sum())
    #aup1g.reset_index(inplace= True)
    #
    #fig_line_1= px.bar(aup1g, x="Brand", y="User_Count", title=f"{year} - BRANDS AND USER COUNT",
    #                   width=800, color_discrete_sequence=px.colors.sequential.haline_r)
    #st.plotly_chart(fig_line_1)

    return aup1

def agg_user_plot_2(df, quarter):
    
    aup2 = df[df["Quarter"] == quarter]
    aup2.reset_index(drop= True, inplace= True)

    fig_pie_1 = px.pie(data_frame=aup2, names= "Brand", values="User_Count",
                       #hover_data= "Percentage",
                       width=800, title=f"{year} Q{quarter} - USER COUNT IN PERCENTAGE", hole=0.5,
                       color_discrete_sequence = px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return aup2

def agg_user_plot_3(df, state):
    
    aup3 = df[df["State"] == state]
    aup3.reset_index(drop= True, inplace= True)

    aup3g= pd.DataFrame(aup3.groupby("Brand")["User_Count"].sum())
    aup3g.reset_index(inplace= True)

    fig_scatter_1= px.line(aup3g, x="Brand", y="User_Count", title = f"{state.upper()} - {year} Q{quarter} - USER COUNT", markers=True, width=800)
    st.plotly_chart(fig_scatter_1)

def map_trans_plot_1(df, state):
    
    mtp1 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    mtp1g = mtp1.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    mtp1g.reset_index(inplace= True)

    #col1,col2= st.columns(2)
    
    #with col1:
    fig_map_trans_bar_1= px.bar(mtp1g, x="District", y="Transaction_Amount",
                                width=600, height=500, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION AMOUNT",
                                color_discrete_sequence= px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_bar_1)

    #with col2:
    fig_map_trans_bar_2 = px.bar(mtp1g, x="District", y="Transaction_Count",
                                 width=600, height=500, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION COUNT",
                                 color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_bar_2)

def map_trans_plot_2(df, state):
    
    mtp2 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    mtp2g = mtp2.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    mtp2g.reset_index(inplace= True)

    #col1,col2= st.columns(2)
    
    #with col1:
    fig_map_trans_pie_1 = px.pie(mtp2g, names="District", values="Transaction_Amount",
                                width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION AMOUNT",
                                hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_pie_1)

    #with col2:
    fig_map_trans_pie_2 = px.pie(mtp2g, names="District", values="Transaction_Count",
                                 width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION COUNT",
                                 hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
    
    st.plotly_chart(fig_map_trans_pie_2)
        
def map_user_plot_1(df, year):
    
    mup1 = df[df["Year"] == year]
    mup1.reset_index(drop= True, inplace= True)
    
    #mup1g = mup1.groupby("State")[["User_Count", "App_Opens"]].sum()
    #mup1g.reset_index(inplace= True)
    #
    #fig_map_user_plot_1 = px.line(mup1g, x="State", y=["User_Count", "App_Opens"], markers=True,
    #                              width=1000, height=800, title= f"{year} - REGISTERED USERS AND APPOPENS",
    #                              color_discrete_sequence=px.colors.sequential.Viridis_r)
    #st.plotly_chart(fig_map_user_plot_1)

    return mup1

def map_user_plot_2(df, quarter):
    
    mup2 = df[df["Quarter"] == quarter]
    mup2.reset_index(drop= True, inplace= True)
    
    mup2g= mup2.groupby("State")[["User_Count", "App_Opens"]].sum()
    mup2g.reset_index(inplace= True)

    fig_map_user_plot_2 = px.line(mup2g, x="State", y=["User_Count", "App_Opens"], markers=True,
                                  title=f"{df['Year'].min()} Q{quarter} - REGISTERED USERS AND APPOPENS",
                                  width=1000, height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_2)

    return mup2

def map_user_plot_3(df, state):
    
    mup3 = df[df["State"] == state]
    mup3.reset_index(drop= True, inplace= True)
    
    mup3g = mup3.groupby("District")[["User_Count", "App_Opens"]].sum()
    mup3g.reset_index(inplace= True)

    #col1,col2= st.columns(2)
    
    #with col1:
        
    fig_map_user_plot_3a = px.bar(mup3g, x="User_Count", y="District", orientation="h",
                                  title=f"{state.upper()} - {year} Q{quarter} - REGISTERED USERS", height=800,
                                  color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_3a)

    #with col2:
        
    fig_map_user_plot_3b = px.bar(mup3g, x="App_Opens", y="District", orientation="h",
                                  title=f"{state.upper()} - {year} Q{quarter} - APPOPENS", height=800,
                                  color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_plot_3b)

def top_trans_plot_1(df, state):
    
    ttp1 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    ttp1g = ttp1.groupby("Pincode")[["Transaction_Count","Transaction_Amount"]].sum()
    ttp1g.reset_index(inplace= True)

    #col1,col2= st.columns(2)
    
    #with col1:
    #fig_top_trans_bar_1= px.bar(ttp1g, x="Pincode", y="Transaction_Amount",
    #                            width=600, height=500, title=f"{state.upper()} PINCODES TRANSACTION AMOUNT",
    #                            color_discrete_sequence= px.colors.sequential.Mint_r)
    #st.plotly_chart(fig_top_trans_bar_1)

    #with col2:
    #fig_top_trans_bar_2 = px.bar(ttp1g, x="Pincode", y="Transaction_Count",
    #                             width=600, height=500, title=f"{state.upper()} PINCODES TRANSACTION COUNT",
    #                             color_discrete_sequence=px.colors.sequential.Mint)
    #st.plotly_chart(fig_top_trans_bar_2)
        
def top_trans_plot_2(df, state):
    
    ttp2 = df[df["State"] == state]
    ttp2g = ttp2.groupby("Pincode")[["Transaction_Count","Transaction_Amount"]].sum()
    ttp2g.reset_index(inplace= True)

    #col1,col2= st.columns(2)
    
    #with col1:
    fig_top_trans_pie_1 = px.pie(ttp2g, names="Pincode", values="Transaction_Amount",
                                width=750, height=500, title=f"{state.upper()} - {year} Q{quarter} - TOP 10 PINCODES (TRANSACTION AMOUNT)",
                                hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_top_trans_pie_1)

    #with col2:
    fig_top_trans_pie_2 = px.pie(ttp2g, names="Pincode", values="Transaction_Count",
                                 width=600, height=500, title=f"{state.upper()} - {year} Q{quarter} - TOP 10 PINCODES (TRANSACTION COUNT)",
                                 hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
    st.plotly_chart(fig_top_trans_pie_2)        
        
def top_user_plot_1(df, year):
    
    tup1 = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
    tup1.reset_index(drop=True, inplace=True)

    tup1g = pd.DataFrame(tup1.groupby(["State","Quarter"])["User_Count"].sum())
    tup1g.reset_index(inplace= True)

    fig_top_user_plot_1 = px.bar(tup1g, x="State", y="User_Count", barmode="group",
                            width=1000, height=800, color_continuous_scale=px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_user_plot_1)

    return tup1

def top_user_plot_2(df, state):
    
    tup2 = df[df["State"] == state]
    tup2.reset_index(drop= True, inplace= True)

    tup2g = pd.DataFrame(tup2.groupby("Quarter")["User_Count"].sum())
    tup2g.reset_index(inplace= True)

    fig_top_user_plot_2 = px.bar(tup2, x="Quarter", y="User_Count", barmode="group",
                            width=1000, height=800, color= "Pincode", hover_data="Pincode",
                            color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_user_plot_2)

def ques1():
    
    q1 = agg_user[["Brand", "User_Count"]]
    q1A = q1.groupby("Brand")["User_Count"].sum().sort_values(ascending=False)
    q1B = pd.DataFrame(q1A).reset_index()

    fig_q1 = px.pie(q1B, values="User_Count", names="Brand", color_discrete_sequence=px.colors.sequential.dense_r,
                    title="Top Mobile Brands by User Count")
    return st.plotly_chart(fig_q1)

def ques2():
    
    q2 = agg_trans[["State", "Transaction_Amount"]]
    q2A = q2.groupby("State")["Transaction_Amount"].sum().sort_values(ascending=True)
    q2B = pd.DataFrame(q2A).reset_index().head(10)

    fig_q2 = px.bar(q2B, x="State", y="Transaction_Amount", title="States with Lowest Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_q2)

def ques3():
    
    q3 = map_trans[["District", "Transaction_Amount"]]
    q3A = q3.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=False)
    q3B = pd.DataFrame(q3A).head(10).reset_index()

    fig_q3 = px.pie(q3B, values="Transaction_Amount", names="District", title="Top 10 Districts with Highest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_q3)

def ques4():
    
    q4 = map_trans[["District", "Transaction_Amount"]]
    q4A = q4.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=True)
    q4B = pd.DataFrame(q4A).head(10).reset_index()

    fig_q4 = px.pie(q4B, values="Transaction_Amount", names="District", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_q4)


def ques5():

    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])
    
    year = st.selectbox("**Select the Year**", agg_trans["Year"].unique())
    quarter = st.selectbox("**Select the Quarter**", agg_trans["Quarter"].unique())
    state = st.selectbox("**Select the State**", agg_trans["State"].unique())

if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.markdown(" ")
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\Phone Pe Ad(720P_HD).mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.markdown(" ")
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD).mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.markdown(" ")
        #st.video("C:\\Users\\vignesh\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD)_2.mp4")


if select == "Data Exploration":
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        
        method = st.radio("**Select the Analysis Method**",["Transaction Analysis", "User Analysis"])

        if method == "Transaction Analysis":
            
            #col1,col2 = st.columns(2)
            
            #with col1:
            #    year = st.slider("**Select the Year**", agg_trans["Year"].min(), agg_trans["Year"].max())

            df_agg_trans_Y = agg_trans_Y(agg_trans, year)

            #col1,col2 = st.columns(2)
            
            #with col1:
            #    quarter = st.slider("**Select the Quarter**", df_agg_trans_Y["Quarter"].min(), df_agg_trans_Y["Quarter"].max())

            df_agg_trans_Y_Q = agg_trans_Y_Q(df_agg_trans_Y, quarter)
            
            #Select the State for Analyse the Transaction type
            #state = st.selectbox("**Select the State**", df_agg_trans_Y_Q["State"].unique())

            agg_trans_type(df_agg_trans_Y_Q, state)


        elif method == "User Analysis":
            
            #year = st.selectbox("Select the Year", agg_user["Year"].unique())
            agg_user_Y = agg_user_plot_1(agg_user, year)

            #quarter = st.selectbox("Select the Quarter", agg_user_Y["Quarter"].unique())
            agg_user_Y_Q = agg_user_plot_2(agg_user_Y, quarter)

            #state = st.selectbox("**Select the State_AU**",agg_user_Y_Q["State"].unique())
            agg_user_plot_3(agg_user_Y_Q,state)

    with tab2:
        
        method = st.radio("**Select the Analysis Method**", ["Map Transaction Analysis", "Map User Analysis"])

        if method == "Map Transaction Analysis":
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #   year = st.slider("**Select the Year**", map_trans["Year"].min(), map_trans["Year"].max())
            #   year = st.selectbox("**Select the Year**", map_trans["Year"].unique())

            #df_map_trans_Y = agg_trans_Y(map_trans, year)

            #col1,col2= st.columns(2)
            
            #with col1:
            #    state = st.selectbox("Select the State", df_map_trans_Y["State"].unique())
            
            df_map_trans_Y = map_trans[map_trans["Year"] == year]
            map_trans_plot_1(df_map_trans_Y, state)
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #    quarter = st.slider("**Select the Quarter**", df_map_trans_Y["Quarter"].min(), df_map_trans_Y["Quarter"].max())
            #    quarter = st.selectbox("**Select the Quarter**", df_map_trans_Y["Quarter"].unique())

            #df_map_trans_Y_Q = agg_trans_Y_Q(df_map_trans_Y, quarter)

            #col1,col2= st.columns(2)
            
            #with col1:
            #    state = st.selectbox("Select the State", df_map_trans_Y_Q["State"].unique())            
            
            df_map_trans_Y_Q = df_map_trans_Y[df_map_trans_Y["Quarter"] == quarter]
            map_trans_plot_2(df_map_trans_Y_Q, state)

        elif method == "Map User Analysis":
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #    year = st.selectbox("**Select the Year**", map_user["Year"].unique())
                
            map_user_Y = map_user_plot_1(map_user, year)

            #col1,col2= st.columns(2)
            
            #with col1:
            #    quarter = st.selectbox("**Select the Quarter**", map_user_Y["Quarter"].unique())
                
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarter)

            #col1,col2= st.columns(2)
            
            #with col1:
            #    state = st.selectbox("**Select the State**", map_user_Y_Q["State"].unique())
                
            map_user_plot_3(map_user_Y_Q, state)

    with tab3:
        
        method = st.radio("**Select the Analysis Method**", ["Top Transaction Analysis", "Top User Analysis"])

        if method == "Top Transaction Analysis":
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #    year = st.slider("**Select the Year**", top_trans["Year"].min(), top_trans["Year"].max())
                
            #df_top_tran_Y = agg_trans_Y(top_trans, year)
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #    quarter = st.slider("**Select the Quarter**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max())

            #df_top_tran_Y_Q = agg_trans_Y_Q(df_top_tran_Y, quarter)
            
            df_top_trans_Y = top_trans[top_trans["Year"] == year]
            top_trans_plot_1(df_top_trans_Y, state)
            
            df_top_trans_Y_Q = df_top_trans_Y[df_top_trans_Y["Quarter"] == quarter]
            top_trans_plot_2(df_top_trans_Y_Q, state)

        elif method == "Top User Analysis":
            
            #col1,col2= st.columns(2)
            
            #with col1:
            #    years = st.selectbox("**Select the Year**", top_user["years"].unique())

            df_top_user_Y = top_user_plot_1(top_user, year)

            #col1,col2= st.columns(2)
            
            #with col1:
            #    state = st.selectbox("**Select the State**", df_top_user_Y["State"].unique())

            df_top_user_Y_S = top_user_plot_2(df_top_user_Y, state)


if select == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
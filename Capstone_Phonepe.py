import mysql.connector as sql
import json
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

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

    return dfy

def agg_trans_Y_Q(df, quarter):
    
    dfyq = df[df["Quarter"] == quarter]
    dfyq.reset_index(drop= True, inplace= True)

    dfyqg = dfyq.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum()
    dfyqg.reset_index(inplace= True)

    fig_q_amount = px.bar(dfyqg, x="State", y="Transaction_Amount", hover_data={'State': True, 'Transaction_Amount': ':,.2f'},
                          title=f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION AMOUNT",
                          width=900, height=900, color_discrete_sequence=px.colors.sequential.Burg_r)
    st.plotly_chart(fig_q_amount)

    fig_q_count = px.bar(dfyqg, x="State", y="Transaction_Count", hover_data={'State': True, 'Transaction_Count': ':,.2f'},
                         title= f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION COUNT",
                         width=900, height=900, color_discrete_sequence=px.colors.sequential.Cividis_r)
    st.plotly_chart(fig_q_count)

    fc = open(r"C:/Users/Admin/Guvi D102_New/India.geojson")
    data = json.load(fc)
    state_names = [feature["properties"]["ST_NM"] for feature in data["features"]]
    state_names.sort()

    fig_india_1= px.choropleth(dfyqg,
                               geojson = data,
                               locations = "State",
                               featureidkey = "properties.ST_NM",
                               color = "Transaction_Count",
                               color_continuous_scale = "Sunsetdark",
                               range_color = (dfyqg["Transaction_Count"].min(),dfyqg["Transaction_Count"].max()),
                               hover_name = "State",
                               hover_data={'State': True, 'Transaction_Amount': ':,.2f', 'Transaction_Count': ':,.2f'},
                               title = f"{dfyq['Year'].min()} Q{quarter} - AGGREGATED TRANSACTION AMOUNT & COUNT",
                               fitbounds = "locations",
                               width = 1000,
                               height = 900)
    fig_india_1.update_geos(visible =False)
    st.plotly_chart(fig_india_1)
    
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
    
    fig_hbar_2 = px.bar(aggds, x="Transaction_Amount", y="Transaction_Type", orientation="h",
                        hover_data={'Transaction_Type': True, 'Transaction_Amount': ':,.2f'},
                        color_discrete_sequence=px.colors.sequential.Greens_r, width=600,
                        title=f"{state.upper()} - {year} Q{quarter} - TRANSACTION TYPES AND TRANSACTION AMOUNT", height=500)
    
    st.plotly_chart(fig_hbar_2)
    st.plotly_chart(fig_hbar_1)
        
def agg_user_plot_1(df, year):
    
    aup1 = df[df["Year"] == year]
    aup1.reset_index(drop= True, inplace= True)
    
    return aup1

def agg_user_plot_2(df, quarter):
    
    aup2 = df[df["Quarter"] == quarter]
    aup2.reset_index(drop= True, inplace= True)

    fig_pie_1 = px.pie(data_frame=aup2, names= "Brand", values="User_Count",
                       #hover_data= "Percentage",
                       width=700, title=f"{year} Q{quarter} - USER COUNT IN PERCENTAGE", hole=0.5,
                       color_discrete_sequence = px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return aup2

def agg_user_plot_3(df, state):
    
    aup3 = df[df["State"] == state]
    aup3.reset_index(drop= True, inplace= True)

    aup3g= pd.DataFrame(aup3.groupby("Brand")["User_Count"].sum())
    aup3g.reset_index(inplace= True)

    fig_scatter_1= px.line(aup3g, x="Brand", y="User_Count", title = f"{state.upper()} - {year} Q{quarter} - USER COUNT", markers=True,
                           hover_data={'Brand': True, 'User_Count': ':,.2f'}, width=800)
    st.plotly_chart(fig_scatter_1)

def map_trans_plot_1(df, state):
    
    mtp1 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    mtp1g = mtp1.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    mtp1g.reset_index(inplace= True)

    fig_map_trans_bar_1= px.bar(mtp1g, x="District", y="Transaction_Amount",
                                width=800, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION AMOUNT",
                                hover_data={'District': True, 'Transaction_Amount': ':,.2f'},
                                color_discrete_sequence= px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_bar_1)

    fig_map_trans_bar_2 = px.bar(mtp1g, x="District", y="Transaction_Count",
                                 width=800, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION COUNT",
                                 hover_data={'District': True, 'Transaction_Count': ':,.2f'},
                                 color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_bar_2)

def map_trans_plot_2(df, state):
    
    mtp2 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    mtp2g = mtp2.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    mtp2g.reset_index(inplace= True)

    fig_map_trans_pie_1 = px.pie(mtp2g, names="District", values="Transaction_Amount",
                                width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION AMOUNT",
                                hover_data={'Transaction_Amount': ':,.2f'},
                                hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_map_trans_pie_1)

    fig_map_trans_pie_2 = px.pie(mtp2g, names="District", values="Transaction_Count",
                                 width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - DISTRICT WISE TRANSACTION COUNT",
                                 hover_data={'Transaction_Count': ':,.2f'},
                                 hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
    
    st.plotly_chart(fig_map_trans_pie_2)
        
def map_user_plot_1(df, year):
    
    mup1 = df[df["Year"] == year]
    mup1.reset_index(drop= True, inplace= True)
    
    return mup1

def map_user_plot_2(df, quarter):
    
    mup2 = df[df["Quarter"] == quarter]
    mup2.reset_index(drop= True, inplace= True)
    
    mup2g= mup2.groupby("State")[["User_Count", "App_Opens"]].sum()
    mup2g.reset_index(inplace= True)

    fig_map_user_plot_2 = px.line(mup2g, x="State", y=["User_Count", "App_Opens"], markers=True,
                                  #hover_data={'State': True, 'User_Count': ':,.2f', 'App_Opens': ':,.2f'},
                                  title=f"{df['Year'].min()} Q{quarter} - REGISTERED USERS AND APPOPENS",
                                  width=1000, height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
    fig_map_user_plot_2.update_traces(mode="markers+lines", hovertemplate=None)
    fig_map_user_plot_2.update_layout(hovermode="x unified")
    st.plotly_chart(fig_map_user_plot_2)

    return mup2

def map_user_plot_3(df, state):
    
    mup3 = df[df["State"] == state]
    mup3.reset_index(drop= True, inplace= True)
    
    mup3g = mup3.groupby("District")[["User_Count", "App_Opens"]].sum()
    mup3g.reset_index(inplace= True)

    fig_map_user_plot_3a = px.bar(mup3g, x="User_Count", y="District", orientation="h",
                                  title=f"{state.upper()} - {year} Q{quarter} - REGISTERED USERS", height=800,
                                  hover_data={'District': True, 'User_Count': ':,.2f'},
                                  color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_3a)

    fig_map_user_plot_3b = px.bar(mup3g, x="App_Opens", y="District", orientation="h",
                                  title=f"{state.upper()} - {year} Q{quarter} - APPOPENS", height=800,
                                  hover_data={'District': True, 'App_Opens': ':,.2f'},
                                  color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_plot_3b)

def top_trans_plot_1(df, state):
    
    ttp1 = df[(df["State"] == state) & (df["Year"] == year) & (df["Quarter"] == quarter)]
    ttp1g = ttp1.groupby("Pincode")[["Transaction_Count","Transaction_Amount"]].sum()
    ttp1g.reset_index(inplace= True)
        
def top_trans_plot_2(df, state):
    
    ttp2 = df[df["State"] == state]
    ttp2g = ttp2.groupby("Pincode")[["Transaction_Count","Transaction_Amount"]].sum()
    ttp2g.reset_index(inplace= True)

    fig_top_trans_pie_1 = px.pie(ttp2g, names="Pincode", values="Transaction_Amount",
                                width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - TOP 10 PINCODES (TRANSACTION AMOUNT)",
                                hover_data={'Transaction_Amount': ':,.2f'},
                                hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_top_trans_pie_1)

    fig_top_trans_pie_2 = px.pie(ttp2g, names="Pincode", values="Transaction_Count",
                                 width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - TOP 10 PINCODES (TRANSACTION COUNT)",
                                 hover_data={'Transaction_Count': ':,.2f'},
                                 hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
    st.plotly_chart(fig_top_trans_pie_2)        
        
def top_user_plot_1(df, year):
    
    tup1 = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
    tup1.reset_index(drop=True, inplace=True)

    tup1g = pd.DataFrame(tup1.groupby(["State","Quarter"])["User_Count"].sum())
    tup1g.reset_index(inplace= True)

    fig_top_user_plot_1 = px.bar(tup1g, x="State", y="User_Count", barmode="group",
                            hover_data={'State': True, 'User_Count': ':,.2f'},
                            title=f"{year} Q{quarter} - USER COUNT BY STATE",
                            width=1000, height=800, color_continuous_scale=px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_user_plot_1)

    return tup1

def top_user_plot_2(df, state):
    
    tup2 = df[df["State"] == state]
    tup2.reset_index(drop= True, inplace= True)

    tup2g = pd.DataFrame(tup2.groupby("Pincode")["User_Count"].sum())
    tup2g.reset_index(inplace= True)

    fig_top_user_plot_2 = px.bar(tup2, x="Pincode", y="User_Count", barmode="group",
                            width=1000, height=800, color= "Pincode", hover_data="Pincode",
                            color_continuous_scale=px.colors.sequential.Magenta)
    
    fig_top_trans_pie_3 = px.pie(tup2g, names="Pincode", values="User_Count",
                                width=900, height=600, title=f"{state.upper()} - {year} Q{quarter} - TOP 10 PINCODES (USER COUNT)",
                                hover_data={'User_Count': ':,.2f'},
                                hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_top_trans_pie_3)

def ques1():
    
    q1 = agg_user[["Brand", "User_Count"]]
    q1A = q1.groupby("Brand")["User_Count"].sum().sort_values(ascending=False)
    q1B = pd.DataFrame(q1A).reset_index().head(10)

    fig_q1 = px.pie(q1B, values="User_Count", names="Brand", color_discrete_sequence=px.colors.sequential.dense_r,
                    title="Top 10 Mobile Brands by User Count")
    return st.plotly_chart(fig_q1)

def ques2():
    
    q2 = agg_trans[["State", "Transaction_Amount"]]
    q2A = q2.groupby("State")["Transaction_Amount"].sum().sort_values(ascending=True)
    q2B = pd.DataFrame(q2A).reset_index().head(10)

    fig_q2 = px.bar(q2B, x="State", y="Transaction_Amount", title="10 States With Lowest Transaction Amount",
                    hover_data={'State': True, 'Transaction_Amount': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_q2)

def ques3():
    
    q3 = map_trans[["District", "Transaction_Amount"]]
    q3A = q3.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=False)
    q3B = pd.DataFrame(q3A).head(10).reset_index()

    fig_q3 = px.pie(q3B, values="Transaction_Amount", names="District", title="Top 10 Districts With Highest Transaction Amount",
                    #hover_data={'District': True, 'Transaction_Amount': ':,.2f'},
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_q3)

def ques4():
    
    q4 = map_trans[["District", "Transaction_Amount"]]
    q4A = q4.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=True)
    q4B = pd.DataFrame(q4A).head(10).reset_index()

    fig_q4 = px.pie(q4B, values="Transaction_Amount", names="District", title="10 Districts With Lowest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_q4)


def ques5():

    q5 = map_user[["State", "App_Opens"]]
    q5A = q5.groupby("State")["App_Opens"].sum().sort_values(ascending=False)
    q5B = pd.DataFrame(q5A).reset_index().head(10)

    fig_q5 = px.bar(q5B, x="State", y="App_Opens", title="Top 10 States With Highest AppOpens",
                    hover_data={'State': True, 'App_Opens': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_q5)

def ques6():
    q6 = map_user[["State", "App_Opens"]]
    q6A = q6.groupby("State")["App_Opens"].sum().sort_values(ascending=True)
    q6B = pd.DataFrame(q6A).reset_index().head(10)

    fig_q6 = px.bar(q6B, x="State", y="App_Opens", title="10 States With Lowest AppOpens",
                    hover_data={'State': True, 'App_Opens': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_q6)

def ques7():
    q7 = agg_trans[["State", "Transaction_Count"]]
    q7A = q7.groupby("State")["Transaction_Count"].sum().sort_values(ascending=True)
    q7B = pd.DataFrame(q7A).reset_index().head(10)

    fig_q7 = px.bar(q7B, x="State", y="Transaction_Count", title= "10 States With Lowest Transaction Count",
                    hover_data={'State': True, 'Transaction_Count': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_q7)

def ques8():
    q8 = agg_trans[["State", "Transaction_Count"]]
    q8A = q8.groupby("State")["Transaction_Count"].sum().sort_values(ascending=False)
    q8B = pd.DataFrame(q8A).reset_index().head(10)

    fig_q8 = px.bar(q8B, x="State", y="Transaction_Count", title="Top 10 States With Highest Transaction Count",
                    hover_data={'State': True, 'Transaction_Count': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_q8)

def ques9():
    q9 = agg_trans[["State", "Transaction_Amount"]]
    q9A = q9.groupby("State")["Transaction_Amount"].sum().sort_values(ascending=False)
    q9B = pd.DataFrame(q9A).reset_index().head(10)

    fig_q9 = px.bar(q9B, x="State", y= "Transaction_Amount", title= "Top 10 States With Highest Transaction Amount",
                    hover_data={'State': True, 'Transaction_Amount': ':,.2f'},
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_q9)

def ques10():
    q10 = map_trans[["District", "Transaction_Amount"]]
    q10A = q10.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=True)
    q10B = pd.DataFrame(q10A).reset_index().head(20)

    fig_dt= px.bar(q10B, x= "District", y= "Transaction_Amount", title= "20 Districts With Lowest Transaction Amount",
                   hover_data={'District': True, 'Transaction_Amount': ':,.2f'},
                   color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts", "About"])
    
if select == "Home":

    col1,col2, = st.columns(2)
    col1.image(Image.open("Phonepe_image2.png"),width = 300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("pulse-video.mp4")

if select == "Data Exploration":
    
    with st.sidebar:
        year = st.selectbox("**Select the Year**", agg_trans["Year"].unique())
        quarter = st.selectbox("**Select the Quarter**", agg_trans["Quarter"].unique())
        state = st.selectbox("**Select the State**", agg_trans["State"].unique())
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        
        method = st.radio("**Select the Analysis Method**",["Transaction Analysis", "User Analysis"])

        if method == "Transaction Analysis":
            
            df_agg_trans_Y = agg_trans_Y(agg_trans, year)

            df_agg_trans_Y_Q = agg_trans_Y_Q(df_agg_trans_Y, quarter)
            
            agg_trans_type(df_agg_trans_Y_Q, state)


        elif method == "User Analysis":
            
            agg_user_Y = agg_user_plot_1(agg_user, year)

            agg_user_Y_Q = agg_user_plot_2(agg_user_Y, quarter)

            agg_user_plot_3(agg_user_Y_Q,state)

    with tab2:
        
        method = st.radio("**Select the Analysis Method**", ["Map Transaction Analysis", "Map User Analysis"])

        if method == "Map Transaction Analysis":
            
            df_map_trans_Y = map_trans[map_trans["Year"] == year]
            map_trans_plot_1(df_map_trans_Y, state)
            
            df_map_trans_Y_Q = df_map_trans_Y[df_map_trans_Y["Quarter"] == quarter]
            map_trans_plot_2(df_map_trans_Y_Q, state)

        elif method == "Map User Analysis":
            
            map_user_Y = map_user_plot_1(map_user, year)

            map_user_Y_Q = map_user_plot_2(map_user_Y, quarter)

            map_user_plot_3(map_user_Y_Q, state)

    with tab3:
        
        method = st.radio("**Select the Analysis Method**", ["Top Transaction Analysis", "Top User Analysis"])

        if method == "Top Transaction Analysis":
            
            df_top_trans_Y = top_trans[top_trans["Year"] == year]
            top_trans_plot_1(df_top_trans_Y, state)
            
            df_top_trans_Y_Q = df_top_trans_Y[df_top_trans_Y["Quarter"] == quarter]
            top_trans_plot_2(df_top_trans_Y_Q, state)

        elif method == "Top User Analysis":
            
            df_top_user_Y = top_user_plot_1(top_user, year)

            df_top_user_Y_S = top_user_plot_2(df_top_user_Y, state)

if select == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Mobile Brands By User Count','States With Lowest Trasaction Amount',
                                 'Districts With Highest Transaction Amount','Districts With Lowest Transaction Amount',
                                 'States With Highest AppOpens','States With Lowest AppOpens','States With Lowest Transaction Count',
                                 'States With Highest Transaction Count','States With Highest Transaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Mobile Brands By User Count":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="States With Highest AppOpens":
        ques5()

    elif ques=="States With Lowest AppOpens":
        ques6()

    elif ques=="States With Lowest Transaction Count":
        ques7()

    elif ques=="States With Highest Transaction Count":
        ques8()

    elif ques=="States With Highest Transaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
        
if select == "About":
    st.image(Image.open("Phonepe_image2.png"),width = 500)
    st.write("---")
    st.write("The Indian digital payments story has truly captured the world's imagination."
             " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
             " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
             "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("about_phonepe.jpg"),width = 400)
        
    with col2:
        st.image(Image.open("about_phonepe1.png"),width = 800)

#importing streamlit library
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


#opening the image
image = Image.open('Logo.png')

#displaying the image on streamlit app
st.image(image)
#Display Title
st.title('Extended Test')
#Daily Level Data
dataframe_daily_level=pd.read_csv("Data_Daily_level.csv")
#Monthly Level Data
Monthly_level_Data=pd.read_csv("Data_Monthly_level.csv")
#Country Level Data
Country_level_Data=pd.read_csv("Merged_Country_level.csv")
#United Sates Level
United_States_Level=pd.read_csv("United_States_level.csv")

for column in Monthly_level_Data.columns[1:]:
    Monthly_level_Data.loc[:,column]=Monthly_level_Data[column].apply(lambda x:x.strip('][').replace("'","").split(','))
    Monthly_level_Data.loc[:,column]=Monthly_level_Data[column].apply(lambda x:[temp.strip() for temp in x])
    try:
        Monthly_level_Data.loc[:,column]=Monthly_level_Data[column].apply(lambda x:[float(temp) for temp in x])
    except:
        pass
#
dataframe=pd.read_csv("Sample_Output_Visualization.csv")

#ROAS
st.header('ROAS')
st.write("A Graph showing comparison between estimated vs actual ROAS(Return on Advertisement spent)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=dataframe_daily_level["Date_Daily_Level"], y=dataframe_daily_level["ROAS (up to date)_smoothened"],mode='lines',name='Up To Date ROAS'))
fig.add_trace(go.Scatter(x=dataframe_daily_level["Date_Daily_Level"], y=dataframe_daily_level["ROAS (estimated)_smoothened"],mode='lines',name='Estimated ROAS'))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="ROAS")
st.plotly_chart(fig, use_container_width=True)


#Advertising Performance and Number of Sign Ups
#DataFrame Preparation
Medium_source=Monthly_level_Data[["Date_Monthly_Level","Source / Medium","Signups_3"]]
Medium_source=Medium_source.explode(["Source / Medium","Signups_3"])
Medium_source=Medium_source[~Medium_source["Signups_3"].isna()]
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.split("/")[0])
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace(".com",""))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace("fb","facebook"))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace("lm.",""))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace("l.",""))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace("m.",""))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.replace("mail.",""))
Medium_source["Source / Medium"]=Medium_source["Source / Medium"].apply(lambda x:x.strip())

#Sign-Ups
sign_ups=Medium_source[["Date_Monthly_Level","Signups_3"]].groupby(["Date_Monthly_Level"]).sum().reset_index()
sign_ups=sign_ups.sort_values(by=["Date_Monthly_Level"])
#Plotting Visual Advertising Performance
st.header('Advertising Performance')
st.write("Trends and Patterns in Advertising Performance & Corresponding Number of Sign-Ups from the prespective of Source/Medium")
fig = px.line(sign_ups, x="Date_Monthly_Level", y="Signups_3")
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Sign Up Count")
st.plotly_chart(fig, use_container_width=True)

#Counter
Counter=Medium_source.groupby(["Source / Medium"]).sum().reset_index()[["Source / Medium","Signups_3"]].sort_values(by=["Signups_3"],ascending=False)
st.write("Aggregated Total Count of Sign-Ups across top 10 Sources")
#Plotting Visual with Number of Sign Ups
fig = px.pie(Counter.head(10), values='Signups_3', names='Source / Medium')
st.plotly_chart(fig, use_container_width=True)

#Time Series 
filteration_condition=Medium_source["Source / Medium"]=="facebook"
filteration_condition_1=Medium_source["Source / Medium"]=="google"
filteration_condition_2=Medium_source["Source / Medium"]=="(direct)"
Facebook=Medium_source[filteration_condition].groupby(["Date_Monthly_Level","Source / Medium"]).sum().reset_index()
Google=Medium_source[filteration_condition_1].groupby(["Date_Monthly_Level","Source / Medium"]).sum().reset_index()
Direct=Medium_source[filteration_condition_2].groupby(["Date_Monthly_Level","Source / Medium"]).sum().reset_index()
#Plotting Time Series Data of The Top 3 Sources
st.write("Time Series Data of The top 3 Sources")
fig = go.Figure()
fig.add_trace(go.Scatter(x=Facebook["Date_Monthly_Level"], y=Facebook["Signups_3"],mode='lines',name='Facebook'))
fig.add_trace(go.Scatter(x=Google["Date_Monthly_Level"], y=Google["Signups_3"],mode='lines',name='Google'))
fig.add_trace(go.Scatter(x=Direct["Date_Monthly_Level"], y=Direct["Signups_3"],mode='lines',name='Direct'))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Sign Up Count")
st.plotly_chart(fig, use_container_width=True)

#Website Traffic Data
st.header('Website Traffic Data')
st.subheader("Operating Systems Aggregated Count")
dataframe_temp_1=Monthly_level_Data[["Operating System","Users_1","Signups_1","Sessions_1","Pageviews_1"]]
dataframe_temp_1=dataframe_temp_1.explode(["Operating System","Users_1","Signups_1","Sessions_1","Pageviews_1"])
dataframe_temp_OS=dataframe_temp_1.groupby(["Operating System"]).sum().reset_index()
dataframe_temp_OS=dataframe_temp_OS.sort_values(by=["Users_1","Signups_1","Sessions_1","Pageviews_1"],ascending=False)
Operating_System=list(dataframe_temp_OS["Operating System"].unique())
fig = go.Figure(data=[
    go.Bar(name="Users", x=Operating_System, y=dataframe_temp_OS["Users_1"].values),
    go.Bar(name="SignUps", x=Operating_System, y=dataframe_temp_OS["Signups_1"].values),
    go.Bar(name="Sessions", x=Operating_System, y=dataframe_temp_OS["Sessions_1"].values),
    go.Bar(name="PageViews", x=Operating_System, y=dataframe_temp_OS["Pageviews_1"].values)
 
])
fig.update_layout(barmode='group')
st.plotly_chart(fig, use_container_width=True)


st.subheader("Android and iOS Time Series Analysis")
st.write("Analysis is based on Users, Signups, Sessions, Page Views and Bounces")
dataframe_temp_2=Monthly_level_Data.explode(["Operating System","Users_1","Signups_1","Sessions_1","Pageviews_1","Bounces_1"])
dataframe_temp_2=dataframe_temp_2[["Date_Monthly_Level","Operating System","Users_1","Signups_1","Sessions_1","Pageviews_1","Bounces_1"]]
dataframe_temp_2=dataframe_temp_2.groupby(["Date_Monthly_Level","Operating System"]).sum().reset_index()
dataframe_temp_2=dataframe_temp_2[dataframe_temp_2["Operating System"].isin(["Android","iOS"])]
chart_data = {
    "Users": px.line(dataframe_temp_2, x='Date_Monthly_Level', y='Users_1', color='Operating System', symbol="Operating System"),
    "Sign Ups": px.line(dataframe_temp_2, x='Date_Monthly_Level', y='Signups_1', color='Operating System', symbol="Operating System"),
    "Sessions": px.line(dataframe_temp_2, x='Date_Monthly_Level', y='Sessions_1', color='Operating System', symbol="Operating System"),
    "Page Views":  px.line(dataframe_temp_2, x='Date_Monthly_Level', y='Pageviews_1', color='Operating System', symbol="Operating System"),
    "Bounces":px.line(dataframe_temp_2, x='Date_Monthly_Level', y='Bounces_1', color='Operating System', symbol="Operating System"),
}
selected_chart = st.selectbox("Select a view", list(chart_data.keys()))
chart = chart_data[selected_chart]
st.plotly_chart(chart)


st.subheader("Region Aggregated Count")
st.write("World Map Analysis")
fig = px.choropleth(
    data_frame=Country_level_Data[Country_level_Data["Users_1"]!=0],
    locations='country',
    locationmode='country names',
    color='Users_1',
    color_continuous_scale='Viridis',
    title='Users',
    range_color=(0,1000000)
)
st.plotly_chart(fig, use_container_width=True)


st.write("United States Analysis")

import plotly.express as px
fig = px.choropleth(United_States_Level,
                    locations='index', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='Users_1',
                    color_continuous_scale="Viridis_r", 
                    
                    )
st.plotly_chart(fig, use_container_width=True)


st.title('Summary of Analysis')

st.write('ROAS')
st.markdown(
""" 
 1. Until February 2023: Both Actual and Estimated Graphs followe a closely similar pattern. 
 2. After February 2023: Both curves experienced a decline but the decline is higher in actual curve with expectations to rise again around April but in actual curve the decrease continued until it started to increase gradually around July. 
"""
)

st.write('Advertising Performance')
st.markdown(
""" 
 1. There is an overall increasing trend in count of sign-ups starting from November 2022
 2. The Top 3 Sources based on Sign-Up Count Aggregation Across time is : a. Facebook  b. Google   c. (direct)  
 3. The Number of Sign-ups coming from Direct Source is stable with higher fluctuation from Google and highest fluctuation in Facebook
 4. Although, Facebook Sign-ups started to increase from November  but these customers have low potential of turning into actual customers because the sign-up increase wasn't translated to increase in corresponding ROAS but on the other side it was declining.
"""
)

st.write('Website Traffic Data')
st.markdown(
""" 
 1. iOS and Android Operating Systems present most of the traffic sources and user engagments portion. 
 2. USA, South Africa and Brazil presents the top three countries among the highest number of users. Targeted Marketing Campaigns shall address the three countries based on tailored marketing startegies to boost the sales
 3. Texas is the highest while Vermont is the lowest from the number of Users in the united States.

"""
)

st.write('Hypothesis Testing')
st.markdown(
""" 
Statistical Hypothesis Testing Validated that decline in ROAS is linked to:  
- Decrease in the Percentage of Active Users. This can be due to  
        a. Drop in Current Product Relevance to existing Customers      
        b. Poor User Experience     
        c. Unappealing Website Contebt
- Increase in PCA. THis can be due to  
        a. Higher Advertising Costs     
        b. Increased Competition among Competitors      
        c. Less Effective Targeting Strategy

"""
)

#Part 3
st.title("Comments on :")
st.header('1. Input Data Sources')
st.write('Colums : ')
st.markdown(
""" 
1. Device Category: It is only mobile with no other devices displayed
2. Exit:  More info is needed about from which page user exited to have better understanding of user behaviour.  
3. Operating System : Only 4 out of the 9 available Operating Systems have enough records to analyze while the rest Operating Systems are ignored because only 1 record exists for each of them. There can be opportunity if extra infomration is extracted from the other OS
4. New Users: New Users Column is identically correlated with Users Column so any change in new users count is reflected as change in Users Count so new users column is dropped
 """
)
st.header('2. Merging Different Data Sources')
st.markdown(
""" 
1. Two Data Sources are at Daily Level and Two Data sources are at Monthly Level so result is two unified data sources. 
2. For Data Sources at Daily Level:   
a. The Two data sources have different numbers of sign-ups. They are close to each other but different count so investigation is needed for the difference reason and vaildity of available data. For our Analysis, we will take average of
both numbers to estimate the total number of sign-ups per month and Column name is set to Average Sign up Value. There are cases where one of both data sources have sign up value while the other don't so the Average Sign up Vale is based on the available data source.  
b. Users, Exits and Sessions are prefectly correlated. This can have one of two indications : Customer behaviours are exactly the same on both expansion and shrinking basis. Correlation between Exits and Sessions is logical because large number of sessions have high Exit Rate so it 
is preferred to be available per webpage in order to understand which webpage users hate most. Therefore, Exits and Sessions will be dropped as they don't offer extra information.
c. ROAS and ROAS (estimated) have multiple outliers and distorted plotted Curve. Outliers are handled by setting a threshold upward fence on both Curves. Then, Savgol Filtering is applied to smoothen out the distortion. 
"""
)
st.header('Exploartory Data Analysis (EDA)')
st.write('Trends and Patterns in Advertising Performance & Number of Sign-Ups :')
st.markdown(
""" 
1. It can be investigated from three different prespectives: 1. Source/Medium   2. Operating System  3. Region. 
2. We will Analyze data based on Source/Medium prespective only.  The Source will be standardized based on major sources(facebook,google,etc..) and data is grouped at this level to analyze corresponding trends and patterns.
3. At An Advanced Level, segmentation can be performed at a detailed level on every channel in the major sources and on other prespectives.
4. Comments:  
 a. Data Starts at September and Ends at June. Analysis can be performed only on monthly or qualrterly basis. With an extra time frame, it can be performed at yearly level.  
 b. Mutliple Sources/Medium  have exactly the same number of sign ups(26) so issue needs to be investigated if the number is actually identical or it is problem related to data collection.  
 c. There are data sources with no sign-up counts so they will be ignore.
"""
)
st.write('Website Traffic Data')
st.markdown(
""" 
Website Traffic Data will be analyzed from two prespectives:  
a. Operating System  :  Android and iOS present the highest traffic operationg system. It can be a valid information of lack of enough information from the other operating systems so further investigation needed to be made.  
b. Region  :  There are different types of data stated in the column region(City, Country or Sub-Country). Data can be aggregated at any of the three region types but for simplicity we will do it at a Country Level with the 
aid of external data sources to get country corresponding to both City and Sub-Country and plot geo-spatial plot. In addition, For the United States it will be done at a City Level. There are region names that can exist in 
different countries so they are dropped due to absence of valid information. In Total, There are 358 Region, out of them only 288 Regions are valid. 
2.To Check User Engagement , we will work on 5 main metrics: Users, Sign Ups, Sessions, Pageviews and Bounces  
Note: Region data at advanced level can be analyzed at yearly level to understand change of performance across different years.
"""
)

  
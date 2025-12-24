import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')

company_list = [
    r'C:\Data\projects\S&P_resources\individual_stocks_5yr\AAPL_data.csv' , 
    r'C:\Data\projects\S&P_resources\individual_stocks_5yr\AMZN_data.csv' , 
    r'C:\Data\projects\S&P_resources\individual_stocks_5yr\GOOG_data.csv' , 
    r'C:\Data\projects\S&P_resources\individual_stocks_5yr\MSFT_data.csv'
    
]


all_data = []

for file in company_list:
    current_df = pd.read_csv(file)
    all_data.append(current_df)

all_data = pd.concat(all_data, ignore_index=True)

all_data['date'] = pd.to_datetime(all_data['date'])

st.set_page_config(page_title= "Stock Analysis Dashboard" 
                   , layout = "wide")
st.title("Stock Analysis Dashboard")
tech_list = all_data['Name'].unique()
st.sidebar.title("Choose a Tech company")

selected_company = st.sidebar.selectbox("Select a stock", tech_list )

company_df = all_data[all_data['Name']==selected_company]
company_df.sort_values('date',inplace=True)


## 1st plot

st.subheader(f"Closing price of {selected_company} Over Time")
fig1 = px.line(company_df, x="date" , y ="close"
        , title = selected_company + " closing prices over time")
st.plotly_chart(fig1 , user_container_width = True)


## 2nd plot
st.subheader(f"Moving average of (10,20,50 days)")
ma_day = [10 ,20 , 50]

for ma in ma_day:
    company_df['close_'+str(ma)] = company_df['close'].rolling(ma).mean()
fig2 = px.line(company_df, x="date" , y =["close","close_10",
       "close_20", "close_50"]
        , title = selected_company + "closing prices with moving average")
st.plotly_chart(fig2 , user_container_width = True)



## 3rd plot

st.subheader(f"Daily Returns for  {selected_company} over time")
company_df['Daily return(in %)'] = company_df['close'].pct_change() * 100
fig3 = px.line(company_df, x="date" , y = "Daily return(in %)"
        , title = selected_company + " Daily Returns")
st.plotly_chart(fig3 , user_container_width = True)


## 4th plot

st.subheader("Resampled Closing Price(Monthly/Quareterly/Yearly)")
             
company_df.set_index('date' , inplace = True)
Resample_option = st.radio("Select Resample Frequency" , ["monthly" , "Quarterly","Yearly"])

if Resample_option == "monthly":
    resampled = company_df['close'].resample('ME').mean()
    
elif Resample_option == "Quarterly":
    resampled = company_df['close'].resample('QE').mean()
    
else:
    resampled = company_df['close'].resample('YE').mean()
    
fig4 = px.line(resampled        , title = selected_company + " " +Resample_option+ " Average Closing Price")
st.plotly_chart(fig4 , user_container_width = True)

## 5th plot
app = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['apple_close'] = app['close']
closing_price['amzn_close'] = amzn['close']
closing_price['goog_close'] = google['close']
closing_price['msft_close'] = msft['close']

fig5 , ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot = True , cmap="coolwarm" , ax = ax)
st.pyplot(fig5)

st.markdown("This is Stock Price Analysis Dashboard screen using Streamlit")


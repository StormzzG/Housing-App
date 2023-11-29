import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title='Housing-StormzzG', page_icon=':house:',layout='wide')

st.title(':house: Housing Project EDA')
st.markdown('<style>div.block-container{padding-top:2rem;}<style>',unsafe_allow_html=True)

fl = st.file_uploader(':file_folder: Upload a File',type=(['csv','txt','xlsx','xls']))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    df = pd.read_csv('ames.csv')

st.header('Focusing on The Three Main Features:')
col1, col2 = st.columns((2))
with col1:
    mean = np.mean(df['TotRmsAbvGrd'])
    median = np.median(df['TotRmsAbvGrd'])
    st.subheader('Total Rooms Above Grade')
    fig = px.histogram(df, x='TotRmsAbvGrd')
    fig.update_layout(bargap=0.2)
    fig.add_vline(x=mean, annotation_text='Mean',line_color='red')
    fig.add_vline(x=median, annotation_text='Median', line_color='green',annotation_position='top left')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    mean = np.mean(df['OverallCond'])
    median= np.median(df['OverallCond'])
    st.subheader('Overall Condition')
    fig = px.histogram(df, x='OverallCond')
    fig.update_layout(bargap=0.2)
    fig.add_vline(x=mean, annotation_text='Mean', line_color='red')
    fig.add_vline(x=median, annotation_text='Median', line_color='green',annotation_position='top left')
    st.plotly_chart(fig,use_container_width=True)

median = np.median(df['SalePrice'])
mean = np.mean(df['SalePrice'])
st.subheader('SalePrice')
fig3 = px.histogram(df, x='SalePrice')
fig3.add_vline(x=median, line_color='green',annotation_text='Median',annotation_position="top left")
fig3.add_vline(x=mean, annotation_text='Mean', line_color='red')
st.plotly_chart(fig3,use_container_width=True)

st.subheader('Correlation of the 3 features using Heatmap')
corr_data = df[['TotRmsAbvGrd', 'OverallCond', 'SalePrice']]
corr_matrix = corr_data.corr()
fig4 = px.imshow(corr_matrix, text_auto=True)
st.plotly_chart(fig4,use_container_width=True)

st.sidebar.header('Choose Filter')
condition = st.sidebar.multiselect('Choose Overall Condition', df['OverallCond'].unique())
if not condition:
    df2 = df.copy()
else:
    df2 = df[df['OverallCond'].isin(condition)]

st.subheader('Effect of Overall Condition on SalePrice')
st.markdown('This histogram shows the distribution of Sale Price based on the condition you have selected on the Sidebar MultiSelect')
mean2 = np.mean(df2['SalePrice'])
median2 = np.median(df2['SalePrice'])
fig5 = px.histogram(df2, x='SalePrice')
fig5.add_vline(x=mean2, annotation_text='Mean', line_color='red')
fig5.add_vline(x=median2, annotation_text='Median', line_color='green',annotation_position='top left')
st.plotly_chart(fig5,use_container_width=True)

st.header('Correlations:')
col3,col4 = st.columns((2))
with col3:
    st.subheader("'Overall Quality' has the Highest Correlation with SalePrice")
    fig = px.box(df, x='OverallQual', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col4:
    st.subheader("'Kitchen Above Grade' has the Lowest Correlation with SalePrice")
    fig = px.box(df, x='KitchenAbvGr', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)

st.header("Engineering a New Feature(Age) and Checking it's Correlation with SalePrice")
st.markdown('Using a Scatter Plot to show Correlation')
df['Age'] = df['YrSold'] - df['YearBuilt']
fig3 = px.scatter(df, x='Age', y='SalePrice')
st.plotly_chart(fig3,use_container_width=True)

st.markdown('Correlation of Age with SalePrice:')
st.write(df['Age'].corr(df['SalePrice']))
st.markdown('A low negative correlation between Age and SalePrice')


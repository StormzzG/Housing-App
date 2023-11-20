import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

st.sidebar.header('Choose Your Filter')

building = st.sidebar.multiselect('Choose Building Class', df['MSSubClass'].unique())
if not building:
    df1 = df.copy()
else:
    df1 = df[df['MSSubClass'].isin(building)]

zoning = st.sidebar.multiselect('Choose Zoning Classification', df['MSZoning'].unique())
if not zoning:
    df2 = df1.copy()
else:
    df2 = df1[df1['MSZoning'].isin(zoning)]

year = st.sidebar.multiselect('Choose Year Sold', df['YrSold'].unique())

condition = st.sidebar.multiselect('Choose Overall Condition', df['OverallCond'].unique())
if not condition:
    df3 = df.copy()
else:
    df3 = df[df['OverallCond'].isin(condition)]

if not building and not zoning and not year:
    filtered_df = df
elif not building and not zoning:
    filtered_df = df[df['YrSold'].isin(year)]
elif not building and not year:
    filtered_df = df[df['MSZoning'].isin(zoning)]
elif not zoning and not year:
    filtered_df = df[df['MSSubClass'].isin(building)]
elif building and zoning:
    filtered_df = df2[(df2['MSSubClass'].isin(building)) & (df2['MSZoning'].isin(zoning))]
elif building and year:
    filtered_df = df1[(df1['MSSubClass'].isin(building)) & (df1['YrSold'].isin(year))]
elif zoning and year:
    filtered_df = df2[(df2['MSZoning'].isin(zoning)) & (df2['YrSold'].isin(year))]
else:
    filtered_df = df2[(df2['MSSubClass'].isin(building)) & (df2['MSZoning'].isin(zoning)) & (df2['YrSold'].isin(year))]

col1, col2, col3 = st.columns((3))
col4, col5, col6 = st.columns((3))
with col1:
    st.subheader('General Zoning Classification')
    fig = px.histogram(filtered_df, x='MSZoning')
    st.plotly_chart(fig,use_container_width=True)
with col2:
    st.subheader('General Lot Shapes')
    fig = px.histogram(filtered_df, x='LotShape')
    st.plotly_chart(fig, use_container_width=True)
with col3:
    st.subheader('General Sale Conditions')
    fig = px.histogram(filtered_df, x='SaleCondition')
    st.plotly_chart(fig, use_container_width=True)
with col4:
    st.subheader('SalePrice')
    fig = px.box(filtered_df, y='SalePrice')
    st.plotly_chart(fig, use_container_width=True)
with col5:
    st.subheader('Total Rooms Above Grade')
    fig = px.histogram(filtered_df, x='TotRmsAbvGrd')
    st.plotly_chart(fig, use_container_width=True)
with col6:
    st.subheader('Overall Conditions')
    fig = px.histogram(filtered_df, x='OverallCond')
    fig.update_layout(xaxis = dict(tickvals = [1,2,3,4,5,6,7,8,9]))
    st.plotly_chart(fig, use_container_width=True)

with st.expander('View Data'):
    st.write(filtered_df.style.background_gradient(cmap='YlOrBr'))
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name='Data1', mime='text/csv')

overallcond = filtered_df.groupby(by = ['OverallCond'], as_index=False)['SalePrice'].sum()

col7, col8 = st.columns((2))
with col7:
    st.subheader('Overall Conditions on SalePrice')
    st.markdown('This Bar Chart shows the distribution of Sale Price based on different Overall Conditions in the DataSet.')
    fig = px.bar(overallcond, x='OverallCond', y='SalePrice')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander('Condition View Data'):
        st.write(overallcond.style.background_gradient(cmap='YlOrBr'))
        csv = overallcond.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Condition CSV', mime='text/csv', help='Download the OverallCondition CSV')
with col8:
    st.subheader('Sale Price Based on Overall Condition')
    st.markdown('This box plot shows distribution of saleprice based on the condition you have chosen in the Overall condition multiselect')
    fig = px.box(df3, y='SalePrice')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander('View Data'):
        st.write(df3.style.background_gradient(cmap='YlOrBr'))
        csv = df3.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Condition CSV', mime='tetx/csv')

corr_data = filtered_df[['LotArea', 'OverallQual', 'OverallCond','YearBuilt','YearRemodAdd', 'FullBath', 'HalfBath', 'TotRmsAbvGrd', 'GarageCars','GarageArea',
                         'MoSold','YrSold','WoodDeckSF','OpenPorchSF','EnclosedPorch','PoolArea','SalePrice']]
corr_matrix = corr_data.corr()
st.subheader('Correlation Between Features and SalePrice')
fig2 = px.imshow(corr_matrix, text_auto=True)
fig2.update_layout(width=1400, height=1200)
st.plotly_chart(fig2, use_container_width=True)

col9,col10,col11 = st.columns((3))
col12,col13,col14 = st.columns((3))
with col9:
    st.subheader('Correlation of 0.79')
    fig = px.scatter(df, x='OverallQual', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col10:
    st.subheader('Correlation of 0.64')
    fig = px.scatter(df, x='GarageCars', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col11:
    st.subheader('Correlation of 0.62')
    fig = px.scatter(df, x='GarageArea', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col12:
    st.subheader('Correlation 0f 0.56')
    fig = px.scatter(df, x='FullBath', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col13:
    st.subheader('Correlation of 0.53')
    fig = px.scatter(df, x='TotRmsAbvGrd', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)
with col14:
    st.subheader('Correlation of 0.52')
    fig = px.scatter(df, x='YearBuilt', y='SalePrice')
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Engineering a New Feature(Age) and Checking it's Correlation with SalePrice")
df['Age'] = df['YrSold'] - df['YearBuilt']
with st.expander('View New Data'):
    st.write(df.style.background_gradient(cmap='YlOrBr'))
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name='New Data',mime='text/csv')

fig3 = px.scatter(df, x='Age', y='SalePrice')
st.plotly_chart(fig3,use_container_width=True)

st.markdown('Correlation of Age with SalePrice:')
st.write(df['Age'].corr(df['SalePrice']))
st.markdown('A low negative correlation between Age and SalePrice')


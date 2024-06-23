import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib
from streamlit_option_menu import option_menu 

st.set_page_config(page_title='Housing-StormzzG', page_icon=':house:',layout='wide')

st.title(':house: Housing Project EDA')
st.markdown('<style>div.block-container{padding-top:3rem;}<style>',unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=['Data Visualization', 'Machine Learning'],
    default_index=0,
    orientation='horizontal'
)

if selected == 'Data Visualization':
    df = pd.read_csv('ames.csv')

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

    # st.sidebar.header('Welcome')

    st.subheader('Effect of Overall Condition on SalePrice')
    condition = st.multiselect('Choose Overall Condition', df['OverallCond'].unique())
    if not condition:
        df2 = df.copy()
    else:
        df2 = df[df['OverallCond'].isin(condition)]
    st.markdown('This histogram shows the distribution of Sale Price based on the condition you have selected.')
    mean2 = np.mean(df2['SalePrice'])
    median2 = np.median(df2['SalePrice'])
    fig5 = px.histogram(df2, x='SalePrice')
    fig5.add_vline(x=mean2, annotation_text='Mean', line_color='red')
    fig5.add_vline(x=median2, annotation_text='Median', line_color='green',annotation_position='top left')
    st.plotly_chart(fig5,use_container_width=True)
    st.write('Mean: ',mean2)
    st.write('Median: ',median2)



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

    st.write('Correlation of Age with SalePrice: ',df['Age'].corr(df['SalePrice']))
    st.markdown('A low negative correlation between Age and SalePrice')

elif selected == 'Machine Learning':
    st.markdown('This housing price predictor has been built on a supervised linear regression machine learning algorithm. The data used to train this model is the same as the one used for analysis. Predict a house price by filling in the requirements below! [Here](https://github.com/StormzzG/machine-learning) is a link to a python notebook used to build this model.')
    st.markdown('<style>div.block-container{padding-bottom: 3rem;}<style>',unsafe_allow_html=True)
    with open('PricePredictor2.joblib', 'rb') as f:
        model = joblib.load(f)

    col1,col2 = st.columns((2))
    with col1:
        year = st.number_input('Year Built')
    with col2:
        rooms = st.number_input('Total Rooms Above Grade(Above Ground)')

    col3,col4 = st.columns((2))
    with col3:
        quality  = st.number_input('Overall Quality')
    with col4:
        garage = st.number_input('Garage Area(sqft)')

    grliv = st.number_input('Above Ground Living Area(sqft)')

    submit_button = st.button('Predict')

    if submit_button:
        if not year and not rooms and not quality and not garage and not grliv:
            st.error('Please fill all requirements')
            prediction = 0
        elif not year:
            st.error('Please fill all requirements')
            prediction = 0
        elif not rooms:
            st.error('Please fill all requirements')
            prediction = 0
        elif not quality:
            st.error('Please fill all requirements')
            prediction = 0
        elif not garage:
            st.error('Please fill all requirements')
            prediction = 0
        elif not grliv:
            st.error('Please fill all requirements')
            prediction = 0
        elif year and rooms and quality and garage and grliv:
            prediction = model.predict([[year, rooms, quality, garage, grliv]])
            st.write(f"Predicted Price: $ {float(np.round(prediction, 2))}")

    st.subheader('Sample Data used for Training and Testing')
    df2 = pd.read_csv('Housing.csv')
    df3 = df2.drop(['OverallCond'], axis=1)
    st.dataframe(df3.head().style.background_gradient(cmap='summer'))
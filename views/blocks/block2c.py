import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd



def createLineChart(df):
   # Create a dropdown for selecting LGAs, including an option for all LGAs
    lga_options = ['All LGAs'] + df['LGA'].unique().tolist()
    selected_lga = st.selectbox('Select LGA', lga_options, index=0)

    # Filter the DataFrame based on the selected LGA
    if selected_lga == 'All LGAs':
        filtered_df = df  # Include all LGAs
    else:
        filtered_df = df[df['LGA'] == selected_lga]

    values = []
    labels = []

    for year in filtered_df['Year'].unique():
        year_data = filtered_df[filtered_df['Year'] == year].copy()
        for quarter in range(1, 5):
            quarter_data = year_data[year_data['Quarter'] == quarter].copy()
            values.append(np.sum(quarter_data['Total'].values))
            labels.append(f"{year} Q{quarter}")

    # Plotting the line graph
    plt.figure(figsize=(10, 5))  # Adjust the width and height as needed

    # Plotting the data
    plt.plot(labels, values, marker='o', linestyle='-')

    # Adding labels and title
    if selected_lga == 'All LGAs':
        plt.title('Tuberculosis cases for All LGAs per quarter and year')
    else:
        plt.title(f'Tuberculosis cases for {selected_lga} per quarter and year')

    plt.xlabel('Quarter')
    plt.ylabel('Total Value')

    plt.xticks(rotation='vertical')

    # Displaying the plot
    st.pyplot(plt)



def vis2C(combined_df):
    allYears = pd.read_csv("Datasets/block2c/block2c_19_to_23_complete.csv")
    createLineChart(allYears)
    year_quarter='2022Q2'
    df = pd.read_csv("Datasets/block2c/Block2C.csv")
    c1, c2 = st.columns(2)
    
    df['Year_Quarter'] = df['Year'].astype('str')+'Q'+df['Quarter'].astype('str')
    df.drop(columns=['Unnamed: 0'],inplace=True)
    fig = px.pie(
        data_frame=df.groupby(['Sex'])['TB_Cases'].sum().reset_index(),
        names = 'Sex',
        values = 'TB_Cases',
        hole = 0.5,
        color_discrete_sequence  = ["blue","skyblue"],
        title = 'Total TB Cases By Gender')
    fig.update_layout(template='plotly_white')
    c2.plotly_chart(fig)

    data = df.groupby(['Year_Quarter','Age_Gr','Sex'])['TB_Cases'].sum().reset_index()

    data = data[data['Year_Quarter']==year_quarter]
    fig = px.bar(
            data_frame = data,
            x = 'Age_Gr',
            y = 'TB_Cases',
            category_orders ={'Age_Gr': ['0-4','5-14','15-24','25-34','35-44','45-54','55-64','>=65']},
            color = 'Sex',
            barmode = 'group',
            color_discrete_sequence=["#636efa", "#ef553b"],
            title = f'Genderwise TB Cases By Age_Gr for quarter {year_quarter}'
        )
    fig.update_layout(template='plotly_white')
    c1.plotly_chart(fig)

    
# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def block2dTBHIV(blockCombined):

    """Groups data by Year_Quarter and Sex, creates a line chart, and returns the figure."""

    grouped_sex_total_df = blockCombined.groupby(['Year_Quarter', 'Sex'], as_index=False)['Total'].sum()
    # grouped_sex_total_df['Year_Quarter'] = grouped_sex_total_df['Year'].astype(str) + '_Q' + grouped_sex_total_df['Quarter'].astype(str)

    fig = px.line(
        grouped_sex_total_df,
        x='Year_Quarter',
        y='Total',
        color='Sex',
        markers=True,
        title='TB-HIV Cases Activity along the years<br><sup>Data Source: block2d - Demographic Breakdown of HIV-Positive TB Cases (by Sex and Age Group)</sup>',
    )

    fig.update_layout(
        xaxis_title='Year and Quarter',
        yaxis_title='Count',
        height=600,
        width=1200,
        showlegend=False
    )

    return fig


# def create_age_group_distribution_chart(blockCombined, data):
        
#         # Melt the DataFrame to transform it into a suitable format for Plotly Express
#         melted_df = pd.melt(
#             blockCombined,
#             id_vars=['Year_Quarter', 'LGA', 'Sex'],
#             value_vars=["0 to 4", "5 to 14", "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65"],
#             var_name='Age_Group',
#             value_name='Values'
#         )

#         # Sum the values grouped by year_quarter, age_group, and sex
#         aggregated_df = melted_df.groupby(["Year_Quarter", "Age_Group", "Sex"], as_index=False)['Values'].sum()

#         # Filter data for the specified year_quarter
#         filtered_df = aggregated_df[aggregated_df["Year_Quarter"] == data]

#         # Create the grouped bar chart
#         chart_title = f"Distribution of TB-HIV Cases by Sex, Age Group in {data}"
#         fig = px.bar(
#             filtered_df,
#             x='Age_Group',
#             y='Values',
#             color='Sex',
#             barmode='group',
#             title=chart_title,
#             category_orders={"Age_Group": ["0 to 4", "5 to 14", "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65"]}
#         )

#         # Customize the layout
#         fig.update_layout(
#             xaxis_title='Age Group',
#             yaxis_title='Count',
#             height=600,
#             width=1200
#         )

#         return fig
def show_gender_age_tb(blockCombined, year_quarter):
    """
    Generates and displays a grouped bar chart showing the distribution of age groups by gender.

    Args:
        blockCombined (pd.DataFrame): The DataFrame containing the data.
        year_quarter (str): The year and quarter for which the data is visualized.

    Returns:
        A Plotly Express figure object representing the grouped bar chart.
    """
    # Melt the DataFrame to transform it into a suitable format for Plotly Express
    melted_df = pd.melt(
        blockCombined,
        id_vars=['Year_Quarter', 'LGA', 'Sex'],
        value_vars=["0 to 4", "5 to 14", "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65"],
        var_name='Age_Group',
        value_name='Values'
    )

    # Sum the values grouped by year_quarter, age_group, and sex
    aggregated_df = melted_df.groupby(["Year_Quarter", "Age_Group", "Sex"], as_index=False)['Values'].sum()

    # Filter data for the specified year_quarter
    filtered_df = aggregated_df[aggregated_df["Year_Quarter"] == year_quarter]

    # Create the grouped bar chart
    chart_title = f"For which sex and age group were the most TB-HIV cases reported in {year_quarter}?<br><sup>Data Source: blockCombined - Demographic Breakdown of HIV-Positive TB Cases (by Sex and Age Group)</sup>"
    fig = px.bar(
        filtered_df,
        x='Age_Group',
        y='Values',
        color='Sex',
        barmode='group',
        title=chart_title,
        category_orders={"Age_Group": ["0 to 4", "5 to 14", "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65"]}
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Count',
        height=600,
        width=1200
    )

    return fig






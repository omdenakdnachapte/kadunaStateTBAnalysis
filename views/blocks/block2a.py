# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


def block2aTBCases(blockCombined):
    """
    Visualize the block2a dataset.
    """
    # total tb cases notified aggregated by quarter
    total_agg = blockCombined['Total TB Cases notified'].groupby(blockCombined['Date']).sum()
    # Create a line chart for the trend of Total TB Cases notified over quarters
    fig = px.line(total_agg, x=total_agg.index, y=total_agg.values, title='Trend of Total TB Cases notified over quarters')
    fig.update_layout(xaxis_title='Quarter', yaxis_title='Total TB Cases notified')
    return fig

def block2aDiagQtr(blockCombined):
    # Subset the relevant columns for comparative analysis
    methods_columns = ['PTB Xpert Positive', 'PTB Smear Positive', 'PTB TB Lamp', 'PTB Clinically Diagnosed (X-ray and others)']
    data_methods = blockCombined[['Date'] + methods_columns]

    # Melt the dataframe to transform it for easier plotting
    data_methods_melted = data_methods.melt(id_vars=['Date'], var_name='Diagnostic Method', value_name='Count')

    # Create a grouped bar chart to compare diagnostic method counts across quarters
    fig = px.bar(data_methods_melted, x='Date', y='Count', color='Diagnostic Method',
             barmode='group', title='Comparison of Diagnostic Methods by Quarter',
             labels={'Count': 'Number of Cases', 'Quarter': 'Quarter'})
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Number of Cases')
    return fig

def block2aDistLGA(blockCombined):
    fig = px.bar(
        blockCombined,
        x='LGA',
        title='Distribution of TB Cases by Local Government Area (LGA)'
    )
    return fig  # Return the Plotly figure

        
# def block2aTotalTBCasesOverTime(blockCombined):
#     fig = px.line(
#         blockCombined,
#         x='Date',
#         y='Total TB Cases notified',
#         title='Time Series Decomposition of Total TB Cases',
#         labels={'Date': 'Date', 'Total TB Cases notified': 'Total TB Cases'},
#     )

#     fig.update_layout(
#         xaxis_title='Date',
#         yaxis_title='Total TB Cases',
#     )

#     return fig

# Function for creating the scatter plot
def block2aReleationship(blockCombined):
    # Select required columns
    selected_columns = [
        'All TB cases who had Xpert test',
        'Total TB Cases notified',
        'LGA',
    ]
    data_selected = blockCombined[selected_columns]

    # Create the scatter plot with Plotly Express
    fig = px.scatter(
        data_selected,
        x="All TB cases who had Xpert test",
        y="Total TB Cases notified",
        size="Total TB Cases notified",
        color="LGA",
        hover_name="LGA",
        title="Relationship between TB Cases with Xpert Test and Total TB Cases",
        labels={
            "All TB cases who had Xpert test": "TB Cases with Xpert Test",
            "Total TB Cases notified": "Total TB Cases",
        },
    )

    # Update axis titles
    fig.update_layout(
        xaxis_title="TB Cases with Xpert Test",
        yaxis_title="Total TB Cases",
    )

    # Show the plot
    return fig  # Return the figure object



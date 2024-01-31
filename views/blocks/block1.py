import matplotlib.pyplot as plt
import streamlit as st
import geopandas as gpd
import pandas as pd
import shap
import plotly.express as px
def vis1A(blockCombined, numYears, numQuarters):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    

    # Total number of presumptives
    axes[0, 0].hist(blockCombined['Total number of presumptives'], bins=20, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Total number of presumptives')
    axes[0, 0].set_xlabel('Number of presumptives')
    axes[0, 0].set_ylabel('Frequency')

    # Total examined with Xpert
    axes[0, 1].hist(blockCombined['Presumptive DS-TB'], bins=20, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('Presumptive DS-TB')
    axes[0, 1].set_xlabel('Number examined with Presumptive DS-TB')
    axes[0, 1].set_ylabel('Frequency')

    # MTB detected
    axes[1, 0].hist(blockCombined['Presumptive DR-TB'], bins=20, color='lightcoral', edgecolor='black')
    axes[1, 0].set_title('Presumptive DR-TB')
    axes[1, 0].set_xlabel('Number of Presumptive DR-TB detected cases')
    axes[1, 0].set_ylabel('Frequency')

    # Total diagnosed
    axes[1, 1].hist(blockCombined['Total diagnosed'], bins=20, color='gold', edgecolor='black')
    axes[1, 1].set_title('Total diagnosed')
    axes[1, 1].set_xlabel('Number of diagnosed cases')
    axes[1, 1].set_ylabel('Frequency')
    

    st.pyplot(fig)


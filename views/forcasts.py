# Import necessary libraries
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import geopandas as gpd
from tqdm.auto import tqdm
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from math import sqrt
# deprecate warnings
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import plotly.graph_objects as go


df = pd.read_csv('Datasets/Misc/PTB_EPTB_Total_lab_clinical_historical_forecasts.csv')

def makeForcast(title):
    
    traces = []
    for lga in df['LGA'].unique():
        lga_data = df[df['LGA'] == lga]

        # Trace for the lower bound of the 95% confidence interval
        trace_lower = go.Scatter(
            x=lga_data['Year-Quarter'],
            y=lga_data[title + ' Actual and Forecast  Lower  95%'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            visible=False  # Hide all traces to start
        )
        traces.append(trace_lower)

        # Trace for the upper bound of the 95% confidence interval
        trace_upper = go.Scatter(
            x=lga_data['Year-Quarter'],
            y=lga_data[title + ' Actual and Forecast  Upper  95%'],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(0,100,80,0.5)',
            line=dict(width=0),
            showlegend=False,
            visible=False  # Hide all traces to start
        )
        traces.append(trace_upper)

        # Trace for the PTB Total Actual and Forecast
        trace = go.Scatter(
            x=lga_data['Year-Quarter'],
            y=lga_data[title + ' Actual and Forecast'],
            mode='lines',
            line=dict(color='blue'),
            name= title + ' notified Actual and Forecast',
            visible=False  # Hide all traces to start
        )
        traces.append(trace)

    # Create a layout with a dropdown menu
    layout = go.Layout(
        title=title + ' Actual and Forecast',
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=['visible', [i//3 == j for i in range(len(traces))]],
                        label='LGA: ' + lga,
                        method='restyle'
                    ) for j, lga in enumerate(df['LGA'].unique())
                ]),
                direction='down',
                pad={'r': 10, 't': 10},
                showactive=True,
                x=0,
                xanchor='left',
                y=1.1,
                yanchor='top'
            ),
        ]
        ,legend=dict(orientation="h", y=-0.2, x=-0.05)
    )

    # Create a figure and add the traces
    fig = go.Figure(data=traces, layout=layout)
    return fig

def forcastDisplay(paramter_not_needed):
    
    PTB = makeForcast("PTB Total")
    EPTB = makeForcast("EPTB Total")
    labDiagnosed = makeForcast("lab diagnosed")
    clinicallyDiagnosed = makeForcast("clinically diagnosed")
    totalTBCasesNotified = makeForcast("Total TB Cases notified")
    
    c1, c2 = st.columns(2)
    
    c1.plotly_chart(PTB, use_container_width=True)
    c2.plotly_chart(EPTB, use_container_width=True)
    c1.plotly_chart(labDiagnosed, use_container_width=True)
    c2.plotly_chart(clinicallyDiagnosed, use_container_width=True)
    st.plotly_chart(totalTBCasesNotified, use_container_width=True)
    




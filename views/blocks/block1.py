import matplotlib.pyplot as plt
import streamlit as st
import geopandas as gpd
import pandas as pd
import shap
import plotly.express as px
import pickle
from catboost import CatBoostRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


def vis1A(blockCombined, numYears, numQuarters):
    # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    

    # # Total number of presumptives
    # axes[0, 0].hist(blockCombined['Total number of presumptives'], bins=20, color='skyblue', edgecolor='black')
    # axes[0, 0].set_title('Total number of presumptives')
    # axes[0, 0].set_xlabel('Number of presumptives')
    # axes[0, 0].set_ylabel('Frequency')

    # # Total examined with Xpert
    # axes[0, 1].hist(blockCombined['Presumptive DS-TB'], bins=20, color='lightgreen', edgecolor='black')
    # axes[0, 1].set_title('Presumptive DS-TB')
    # axes[0, 1].set_xlabel('Number examined with Presumptive DS-TB')
    # axes[0, 1].set_ylabel('Frequency')

    # # MTB detected
    # axes[1, 0].hist(blockCombined['Presumptive DR-TB'], bins=20, color='lightcoral', edgecolor='black')
    # axes[1, 0].set_title('Presumptive DR-TB')
    # axes[1, 0].set_xlabel('Number of Presumptive DR-TB detected cases')
    # axes[1, 0].set_ylabel('Frequency')

    # # Total diagnosed
    # axes[1, 1].hist(blockCombined['Total diagnosed'], bins=20, color='gold', edgecolor='black')
    # axes[1, 1].set_title('Total diagnosed')
    # axes[1, 1].set_xlabel('Number of diagnosed cases')
    # axes[1, 1].set_ylabel('Frequency')
    

    # st.pyplot(fig)

    # st.write("regression models")
    # data = pd.read_csv('Datasets/block1a/block1a_19_to_23_complete.csv', index_col=0)
    # X = data.drop(['Total diagnosed', 'Year_Quarter'], axis=1)
    # y = data['Total diagnosed']
    # model = pickle.load(open('pkl_files/model.pkl', 'rb'))
    # y_pred = model.predict(X)

    # # Create a Streamlit app
    # st.title('Predictions vs. Actuals')

    # # Plot predictions vs. actual values using Matplotlib
    # fig, ax = plt.subplots()
    # ax.scatter(y, y_pred)
    # ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    # ax.set_xlabel('Actual')
    # ax.set_ylabel('Predicted')
    # ax.set_title('Predictions vs. Actuals')

    # # Display the plot in the Streamlit app
    # st.pyplot(fig)

    preprocessor = ColumnTransformer(
    transformers=[
            ('onehot', OneHotEncoder(), ['LGA']),
        ],
        remainder='passthrough'  # passthrough features not listed in transformers
    )

    # Define pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', CatBoostRegressor(iterations=200, depth=4, learning_rate=0.1540701057187543))
    ])
    
    data = pd.read_csv('Datasets/block1a/block1a_19_to_23_complete.csv', index_col=0)
    X = data.drop(['Total diagnosed', 'Year_Quarter'], axis=1)
    y = data['Total diagnosed']
    #model = pickle.load(open('pkl_files/model.pkl', 'rb'))
    
    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the pipeline
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X)

    # Ensure y and y_pred are numeric
    # y = pd.to_numeric(y, errors='coerce')
    # y_pred = pd.to_numeric(y_pred, errors='coerce')

    # Plot predictions vs. actual values
    # plt.scatter(y, y_pred)
    # plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    # plt.xlabel('Actual')
    # plt.ylabel('Predicted')
    # plt.title('Predictions vs. Actual')

    # # Show the plot
    # st.write("Regression Models")
    # st.pyplot()

    fig, ax = plt.subplots()

    # Plotting
    ax.scatter(y, y_pred)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    ax.set_title('Regression Model')
    st.pyplot(fig)


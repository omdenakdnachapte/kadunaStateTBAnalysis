import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import math


AllNumCases = {
    '0-4': None,
    '5-14': None, 
    '15-24': None, 
    '25-34':None,
    '35-44': None,
    '45-54': None,
    '55-64': None,
    '>=65': None,
    'Total Cases': None
}

def fillDictionary(df_filled,dictionary):
    dictionary['Total Cases'] = np.sum(pd.to_numeric(df_filled['Total'].values, errors='coerce'))
    dictionary['0-4'] = np.sum(pd.to_numeric(df_filled['0-4'].values, errors='coerce'))
    dictionary['5-14'] = np.sum(pd.to_numeric(df_filled['5-14'].values, errors='coerce'))
    dictionary['15-24'] = np.sum(pd.to_numeric(df_filled['15-24'].values, errors='coerce'))
    dictionary['25-34'] = np.sum(pd.to_numeric(df_filled['25-34'].values, errors='coerce'))
    dictionary['35-44'] = np.sum(pd.to_numeric(df_filled['35-44'].values, errors='coerce'))
    dictionary['45-54'] = np.sum(pd.to_numeric(df_filled['45-54'].values, errors='coerce'))
    dictionary['55-64'] = np.sum(pd.to_numeric(df_filled['55-64'].values, errors='coerce'))
    dictionary['>=65'] = np.sum(pd.to_numeric(df_filled['>=65'].values, errors='coerce'))

def displayBarGraph(df_table, timePeriod=""):
    st.write()
    fig, ax = plt.subplots()
    df_table.drop('Total Cases', axis=1).T.plot(kind='bar', stacked=False, color=['purple', 'blue', 'pink'], ax=ax)
    ax.set_ylabel('Number of Cases')
    ax.set_xlabel('Age Group')
    plt.title('Number of Tuberculosis cases for ' + timePeriod)

    # Display the plot in Streamlit
    #st.pyplot(fig)
    return fig
   

def createPieCharts(dfWhole):
    df = dfWhole.drop(columns=["Total Cases"])
    columns = df.columns.tolist()
    num_columns = len(columns)
    index = -1
    fig, row = plt.subplots( 1, min(num_columns, 4), figsize=(15, 4) )
   
    for ageRange in columns:
        if index == 3:
            index = 0
        
            fig, row = plt.subplots( 1, 4, figsize=(15, 4) )
        else:
            index = index+1  
            
        totalCasesDF = df[[ageRange]]
        totalCasesDF = totalCasesDF.drop("Total")
        totalCasesDF = totalCasesDF.reset_index()
        values = totalCasesDF[ageRange].values
        values = np.nan_to_num(values, nan=0.0)
        labels = totalCasesDF['index'].values
        row[index].pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        row[index].set_title('Pie Chart for ages ' + ageRange)

    return fig


def createPieChartTotal(dfWhole, timePeriod=""):
    totalCasesDF = dfWhole[["Total Cases"]]
    totalCasesDF = totalCasesDF.drop("Total")
    totalCasesDF = totalCasesDF.reset_index()
    values = totalCasesDF["Total Cases"].values
    labels = totalCasesDF['index'].values
    fig, row = plt.subplots( 1, 1, figsize=(15, 4) )
    row.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    row.set_title('Pie chart for all ages for ' + timePeriod)
    #st.pyplot(fig)
    return fig

def analyzeDataFrame(eda2B, bargraph, piechart, chart, totalChart,timePeriod=""):   
    eda2BFemale = eda2B[eda2B ['Sex'] == 'Female'].copy() # This data frame contains all the female data
    eda2BMale = eda2B[eda2B ['Sex'] == 'Male'].copy() # This data frame contains all the male data
    
    # Creates a dictionary that contains information about all the cases for different age groups for both genders combined 
    totalCases = AllNumCases.copy()
    fillDictionary(eda2B,totalCases)

    # Creates a dictionary that contains information about all the cases for different age groups for males 
    maleCases = AllNumCases.copy()
    fillDictionary(eda2BMale ,maleCases)

    # # Creates a dictionary that contains information about all the cases for different age groups for males 
    femaleCases = AllNumCases.copy()
    fillDictionary(eda2BFemale ,femaleCases)
    
    maleDF = pd.DataFrame(maleCases, index=['Male'])
    femaleDF = pd.DataFrame(femaleCases, index=['Female'])
    totalDF = pd.DataFrame(totalCases, index=['Total'])
    combinedDF = pd.concat([totalDF,maleDF, femaleDF])

    
    if bargraph:
        return displayBarGraph(combinedDF, timePeriod)
    elif chart: 
        pd.DataFrame(combinedDF)
        return combinedDF
    elif piechart:
        return createPieCharts(combinedDF)
    else :
        return createPieChartTotal(combinedDF,timePeriod)

        

def vis2B(combined_df):
    # st.write("visualizations for tb cases broken down by gender and age.")
    histogram = analyzeDataFrame(combined_df,True, False, False, False, "")
    totalPiechart = analyzeDataFrame(combined_df, False, False, False, True, "All ages")
    piecharts = analyzeDataFrame(combined_df, False, True, False, False, "Percentage of men and women")
    # numbers = analyzeDataFrame(combined_df,False, False, True, False, "")

    # st.dataframe(numbers)
    c1, c2 = st.columns(2)
    # stats = analyzeDataFrame(combined_df,False, False, True, False)

    # c1.dataframe(stats)
    c1.pyplot(histogram)
    c2.pyplot(totalPiechart)
    st.pyplot(piecharts)
    
import streamlit as st
import altair as alt

# Page configuration
st.set_page_config(
    page_title = "Kaduna State Tuberculosis",
    page_icon = "❤️",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# alt.themes.enable("dark")


st.title('Tuberculosis Analysis in Kaduna')
# st.sidebar.success("Selected page.")

# Sidebar for Slected Year
with st.sidebar:
    st.sidebar.image("images/Kaduna chapter logo.jpg")
    st.title("❤️ Kaduna State Tuberculosis Dashboard")

    if st.button("Contact Us"):
        st.write("""
                **Contact:**
            * Jamaludeen Madaki
            * Omdena Kaduna Chapter Lead
            * omdenakdnachapter@gmail.com
            * +234 7010412114
            """)

st.write("""

This section is dedicated to the Python program that performs an Extract, Transform, Load (ETL) process on the Standard Excel dataset of Tuberculosis (TB) cases in Kaduna. The dataset is structured with multiple sheets, each representing data for a specific Local Government Area (LGA).

The ETL process implemented here serves two main purposes:

- **Extract:** The code reads data from an Excel file, extracting information from multiple sheets within the file. Each sheet corresponds to a specific LGA.

- **Transform:** The extracted data is then transformed. This involves selecting specific rows and columns, inserting new data, renaming columns, and preparing the data in a format that is suitable for further analysis or processing.

- **Load:** Finally, the transformed data is loaded into a pandas DataFrame. This DataFrame can be used for further data analysis tasks or can be saved in a different format like CSV for other uses.

ETL Pipeline is an essential part of our data preprocessing pipeline, turning raw, multi-sheet Excel data into a clean, single-table format that’s easier to work with for downstream tasks such as data analysis and machine learning. By automating this process in a Streamlit application, we ensure that our data preprocessing is reproducible and consistent, saving us time and reducing the potential for manual errors. 
""")
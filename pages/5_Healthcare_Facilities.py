import streamlit as st
import pandas as pd
import plotly.express as px
from views.facilities import make_tb_facilities_plot, get_hiv_cluster_plot, get_tb_cluster_plot

# Page configuration
st.set_page_config(
    page_title = "Kaduna State Tuberculosis",
    page_icon = "❤️",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

#Sidebar for Slected Year
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


st.title('Kaduna Healthcare Facilities Visualizations')

# st.subheader("TB Cases by Facilities")
# with st.container():
#     with st.spinner("Loading..."):
#         st.plotly_chart(make_tb_facilities_plot(), use_container_width=True)

st.subheader("TB Cases by Facilities")
st.markdown("These maps show spatiotemporal clusters of healthcare facilities. Clusters were identified using [ST-DBSCAN](https://www.sciencedirect.com/science/article/pii/S0169023X06000218) algorithm.")
st.markdown("* LGA regions are color coded per legend")
st.markdown("* Points represent individual healthcare facilities and are color coded by their spatiotemporal cluster designation")
st.markdown("* Point sizes are indicative of TB disease burden")
st.markdown("* A st_dbscan_label of -1 indicates these facilities do not fall within a cluster")

# c1_stdb, c2_stdb = st.columns(2)
with st.container():
    st.subheader("Total TB Cases")
    with st.spinner("Loading..."):
        st.plotly_chart(get_tb_cluster_plot(), use_container_width=True)

with st.container():
    st.subheader("HIV and TB Co-infections by Facility")
    with st.spinner("Loading..."):
        st.plotly_chart(get_hiv_cluster_plot(), use_container_width=True)
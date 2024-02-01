import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
from sklearn.neighbors import NearestNeighbors
from st_dbscan import ST_DBSCAN
import pickle


# Read Facilities Data

df = pd.read_excel("Datasets/Misc/TB_all_facility.xlsx", index_col=False)

df['time'] = df.year + (df.quarter - 1)*0.25
df['presumptive_positivity_rate'] = df['presumptive_total_diagnosed']/df['presumptive_examined_for_diagnosis']
df['hiv_tb_pos_rate'] = (df['previously_known_hiv_status_positive'] + df['previously_unknown_hiv_status_tested_for_hiv_positive']) / \
(df['previously_known_hiv_status_positive'] + df['previously_unknown_hiv_status_tested_for_hiv_positive'] + df['previously_known_hiv_status_negative'] + \
df['previously_unknown_hiv_status_tested_for_hiv_negative'])
df['hiv_tb_pos_rate_2'] = df['presumptive_hiv_status_positive']/ (df['presumptive_hiv_status_positive'] + df['presumptive_hiv_status_negative'] + df['presumptive_hiv_status_unknown'])
df['hiv_n_positive'] = (df['previously_known_hiv_status_positive'] + df['previously_unknown_hiv_status_tested_for_hiv_positive'])
df['Year_Quarter'] = df['year'].astype(str) + ' Q' + df['quarter'].astype(str)

# Read Geospatial Shapefile

f = r"nga_adm_osgof_20190417/nga_admbnda_adm2_osgof_20190417.shp" 
shapes = gpd.read_file(f)

rename_ADM2 = {
    'Birnin-Gwari':'Birin Gwari', 
    "Jema'a":'Jemaa', 
    'Kaduna North':'Kaduna north',
    'Kaduna South':'Kaduna south',
    'Markafi':'Makarfi',
    'Sabon-Gari':'Sabon Gari',
    'Zango-Kataf':'Zangon kataf'
}

shapes['ADM2_EN'] = shapes['ADM2_EN'].replace(rename_ADM2)


def get_quarterly_df(facilities_df=df):
    '''
    Calculate quarterly summaries for each LGA by summing across facilities
    '''
    quarterly_df = (facilities_df[['year', 'quarter', 'lga',
                        'total_tb_cases', 'presumptive_total_diagnosed', 'presumptive_examined_for_diagnosis',
                        'previously_known_hiv_status_positive', 'previously_unknown_hiv_status_tested_for_hiv_positive',
                        'previously_known_hiv_status_negative', 'previously_unknown_hiv_status_tested_for_hiv_negative',
                        'previously_unknown_hiv_status_not_tested',
                        'presumptive_hiv_status_positive', 'presumptive_hiv_status_negative', 'presumptive_hiv_status_unknown']]
                    .groupby(['year', 'quarter', 'lga'])
                    .sum()
                    .reset_index()
                    .merge(shapes, left_on='lga', right_on='ADM2_EN', how='left')
                    )
    quarterly_df['time'] = quarterly_df.year + (quarterly_df.quarter - 1)*0.25
    quarterly_df['presumptive_positivity_rate'] = quarterly_df['presumptive_total_diagnosed']/quarterly_df['presumptive_examined_for_diagnosis']
    quarterly_df['hiv_tb_pos_rate'] = (quarterly_df['previously_known_hiv_status_positive'] + quarterly_df['previously_unknown_hiv_status_tested_for_hiv_positive']) / \
        (quarterly_df['previously_known_hiv_status_positive'] + quarterly_df['previously_unknown_hiv_status_tested_for_hiv_positive'] + quarterly_df['previously_known_hiv_status_negative'] + \
    quarterly_df['previously_unknown_hiv_status_tested_for_hiv_negative'])
    quarterly_df['hiv_tb_pos_rate_2'] = quarterly_df['presumptive_hiv_status_positive']/ (quarterly_df['presumptive_hiv_status_positive'] + quarterly_df['presumptive_hiv_status_negative'] + quarterly_df['presumptive_hiv_status_unknown'])

    quarterly_df = gpd.GeoDataFrame(quarterly_df)
    quarterly_df['Year_Quarter'] = quarterly_df['year'].astype(str) + ' Q' + quarterly_df['quarter'].astype(str)
    return(quarterly_df)


def make_tb_spatial_cluster_plot(facilities_df=df, eps1=15000, eps2=0.3, min_samples=5):
    '''
    This function takes a facilities dataset and performs ST-DBSCAN to get spatiotemporal clusters and returns a plotly
    interactive visualization of tuberculosis cases clusters grouped by facilities.
    '''
    tb_df = gpd.GeoDataFrame(facilities_df,
                      geometry=gpd.points_from_xy(facilities_df.lat,facilities_df.lon),
                      crs="EPSG:4326") # ellipsoid projection
    tb_df.geometry = tb_df.geometry.to_crs("EPSG:32650") # converting to flat earth projection with distances in meters
    tb_df['x'] = tb_df.geometry.x
    tb_df['y'] = tb_df.geometry.y
    # for STDBSCAN repeat rows n times where n is number of cases for the facility
    tb_df = tb_df.reindex(tb_df.index.repeat(tb_df.total_tb_cases)).reset_index(drop=True)
    tb_df = tb_df.dropna(subset=['x', 'y'])
    data = tb_df.loc[:, ['time','x','y']].values # transform to numpy array

    tb_df['st_dbscan_label'] = st_dbscan0.labels

    # Implement spatiotemporal DBSCAN
    st_dbscan0 = ST_DBSCAN(eps1 = eps1, eps2 = eps2, min_samples = min_samples)
    st_dbscan0.fit(data)

    tb_df.geometry = tb_df.geometry.to_crs("EPSG:4326") #convert back to ellipsoid projection
    tb_df = tb_df.drop_duplicates().reset_index(drop=True) #remove duplicate rows added for DBSCAN
    tb_df['st_dbscan_label'] = tb_df.st_dbscan_label.astype('string')
    tb_df['Year_Quarter'] = tb_df.Year_Quarter.astype('category')

    quarterly_df = get_quarterly_df(facilities_df)

    fig1 = px.choropleth(quarterly_df,
                         geojson=quarterly_df.geometry,
                        locations=quarterly_df.index,
                        color='total_tb_cases',
                        hover_name = 'ADM2_EN',
                        hover_data = 'presumptive_positivity_rate',
                        color_continuous_scale = 'plasma',
                        projection="mercator",
                        labels='Total TB Cases',
                        animation_frame='Year_Quarter',
                        range_color=[0,1000])
    fig2 = px.scatter_geo(tb_df.sort_values(by="Year_Quarter"), lat="lat", lon="lon", 
                        size="total_tb_cases",
                        color='st_dbscan_label',
                        color_discrete_sequence= px.colors.qualitative.Alphabet,
                        hover_name="name_of_facility",
                        hover_data = 'presumptive_positivity_rate',
                        animation_frame='Year_Quarter')

    fig2.update_layout(showlegend=False)

    for i in range(len(fig2.data)):
        fig2.data[i].showlegend = False
        fig1.add_trace(fig2.data[i])

    for i, frame in enumerate(fig1.frames):
        for j,d in enumerate(fig2.frames[i].data):
            fig2.frames[i].data[j].showlegend = False
            fig1.frames[i].data += (fig2.frames[i].data[j],)

    fig1.update_layout(autosize=False,width=800,height=600)
    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_layout(
        title=dict(text="Total TB Cases Over Time")
    )
    fig1["layout"].pop("updatemenus")
    return(fig1)

def make_hiv_spatial_cluster_plot(facilities_df, eps1=20000, eps2=0.3, min_samples=5):
    '''
    This function takes a facilities dataset and performs ST-DBSCAN to get spatiotemporal clusters and returns a plotly
    interactive visualization of clusters of facilities recording HIV positive cases.
    '''
    df = gpd.GeoDataFrame(facilities_df,
                          geometry=gpd.points_from_xy(facilities_df.lat,facilities_df.lon),
                          crs="EPSG:4326")
    df.geometry = df.geometry.to_crs("EPSG:32650")
    df['x'] = df.geometry.x
    df['y'] = df.geometry.y

    # HIV TB positivity rate is undefined when no HIV+ TB cases observed in that facility
    hiv_df = df.dropna(subset=['hiv_tb_pos_rate'])[['x', 'y', 'time', 'hiv_n_positive']][df['hiv_n_positive'] > 0].reset_index(drop=True)
    # Repeat rows based on HIV n positive since there are multiple individuals at a given facility 
    hiv_df = hiv_df.reindex(hiv_df.index.repeat(hiv_df.hiv_n_positive)).reset_index(drop=True)
    hiv_df = hiv_df.dropna(subset=['x', 'y'])
    data = hiv_df.loc[:, ['time','x','y']].values # transform to numpy array
    st_dbscan = ST_DBSCAN(eps1 = eps1, eps2 = eps2, min_samples = min_samples)
    st_dbscan.fit(data)
    hiv_df['st_dbscan_label'] = st_dbscan.labels
    df = df.merge(hiv_df.drop_duplicates().reset_index(drop=True), on=['x', 'y', 'time', 'hiv_n_positive'], how='left')
    df['st_dbscan_label'] = df.st_dbscan_label.astype('string')
    df['Year_Quarter'] = df.Year_Quarter.astype('category')
    
    quarterly_df = get_quarterly_df(facilities_df)
    
    fig3 = px.choropleth(quarterly_df,
                         geojson=quarterly_df.geometry,
                         locations=quarterly_df.index,
                         color='hiv_tb_pos_rate',
                         hover_name = 'ADM2_EN',
                        #  hover_data = 'hiv_n_positive',
                         color_continuous_scale = 'plasma',
                         projection="mercator",
                         labels='HIV Positive',
                         animation_frame='Year_Quarter',
                         range_color=[0,0.4],
                         )
    fig4 = px.scatter_geo(df.dropna(subset=['st_dbscan_label']).sort_values(by='Year_Quarter'), lat="lat", lon="lon", 
                          size="hiv_tb_pos_rate",
                          color='st_dbscan_label',
                          color_discrete_sequence= px.colors.qualitative.Alphabet,
                          hover_name="name_of_facility",
                          hover_data = 'hiv_n_positive',
                          animation_frame='Year_Quarter')
    fig4.update_layout(showlegend=False)


    for i in range(len(fig4.data)):
        fig4.data[i].showlegend = False
        fig3.add_trace(fig4.data[i])


    for i, frame in enumerate(fig3.frames):
        for j,d in enumerate(fig4.frames[i].data):
            fig4.frames[i].data[j].showlegend = False
            fig3.frames[i].data += (fig4.frames[i].data[j],)

    fig3.update_layout(autosize=False,width=800,height=600)
    fig3.update_geos(fitbounds="locations", visible=False)
    fig3.update_layout(
        title=dict(text="Total HIV Positivity Rate Among TB Cases")
    )
    fig3["layout"].pop("updatemenus")
    return(fig3)


def make_tb_facilities_plot(facilities_df=df):
    df = facilities_df
    quarterly_df = get_quarterly_df(facilities_df)
    fig = px.choropleth(quarterly_df,
                    geojson=quarterly_df.geometry,
                    locations=quarterly_df.index,
                    color='total_tb_cases',
                    hover_name = 'ADM2_EN',
                    hover_data = 'presumptive_positivity_rate',
                    color_continuous_scale = 'plasma',
                    projection="mercator",
                    labels='Total TB Cases',
                    animation_frame='Year_Quarter',
                    range_color=[0,1000])
    fig0 = px.scatter_geo(df, lat="lat", lon="lon", 
                          size="total_tb_cases",
                          hover_name="name_of_facility",
                          hover_data = 'presumptive_positivity_rate',
                          animation_frame='Year_Quarter')
    fig.add_trace(fig0.data[0])
    for i, frame in enumerate(fig.frames):
        fig.frames[i].data += (fig0.frames[i].data[0],)

    fig.update_layout(autosize=False,width=800,height=600)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=dict(text="Total TB Cases Over Time")
    )
    fig["layout"].pop("updatemenus")
    return(fig)

def get_tb_cluster_plot():
    '''
    This function uses saved plotly image of TB cluster plot using 2019 - 2023 Q2 data
    '''
    with open('pkl_files/tb_cluster.pkl', 'rb') as inp:
        tb_cluster = pickle.load(inp)
    return(tb_cluster)

def get_hiv_cluster_plot():
    '''
    This function uses saved plotly image of HIV cluster plot using 2019 - 2023 Q2 data
    '''
    with open('pkl_files/hiv_cluster.pkl', 'rb') as inp:
        hiv_cluster = pickle.load(inp)
    return(hiv_cluster)
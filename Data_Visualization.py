import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Data Visualization", page_icon = ":bar_chart:", layout='wide')
st.markdown('<style>div.block-container{padding-top:10px;}<style>', unsafe_allow_html=True)
st.title("AI Global Index")

df = pd.read_csv("C:\\Users\Lara\Downloads\Streamlit\AI_index_db.csv")
st.title("Overview")
col1, col2, col3 = st.columns([1, 1, 1])


def plot_donut_chart(df, filter_column, height=250, width=250):
    dfg = df[filter_column].value_counts().reset_index()
    dfg.columns = [filter_column, 'Quantity']
    fig = px.pie(dfg, values='Quantity', names=filter_column, hole=0.4, height=height, width=width)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    fig.update_traces(textinfo='text')
    fig.data[0].text = dfg['Quantity'].astype(str)

    st.plotly_chart(fig, use_container_width=True)


def plot_top_10_countries(df, selected_score, title, height=400):
    top_10_countries = df.sort_values(selected_score, ascending=False)[['Country', selected_score]][:10]
    fig = px.bar(
        top_10_countries,
        x='Country',
        y=selected_score,
        color='Country',
        labels={'Country': 'Country Name', selected_score: selected_score},
        title=f'Top 10 Countries by {title}',
    )
    fig.update_xaxes(title_text='Country Name')
    fig.update_yaxes(title_text=selected_score)
    
    st.plotly_chart(fig, use_container_width=True)

with col1:
    #Overview
    st.write("Region Distribution")
    plot_donut_chart(df, 'Region', height=260, width=250)
    st.write("Cluster Distribution")
    plot_donut_chart(df, 'Cluster', height=260, width=250)
    st.write("Income Group Distribution")
    plot_donut_chart(df, 'Income group', height=260, width=250)
    st.write("Political Regime")
    plot_donut_chart(df, 'Political regime', height=260, width=250)

with col2:
    #Bar Chart
    st.markdown(f"<h2 style='font-size: 30px;'>Top 10 Countries</h2>", unsafe_allow_html=True)
    selected_score = st.selectbox('Select Score Category:',
                                  ['Talent', 'Infrastructure', 'Operating Environment',
                                   'Research', 'Development', 'Government Strategy',
                                   'Commercial', 'Total score'])
    if "Country" in df.columns:
        plot_top_10_countries(df, selected_score, selected_score, height=350)

    #Heatmap
    st.markdown(f"<h2 style='font-size: 30px;'>Correlation between Numerical Values</h2>", unsafe_allow_html=True)
    sns.set_theme(style="darkgrid")
    plt.style.use('dark_background')
    st.markdown("""
    <div style="display: flex;">
    </div>
    """, unsafe_allow_html=True)
    # Your code for generating the heatmap
    d = df[['Talent', 'Infrastructure', 'Operating Environment', 'Research', 'Development', 'Government Strategy', 'Commercial', 'Total score']]
    cor = d.corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    mask = np.triu(np.ones_like(cor, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(cor, mask=mask, cmap=cmap, annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": .7})
    # Display the plot
    st.pyplot(fig, use_container_width=True)
   
with col3:
    #Scatter Geo World Map
    # Function to create scatter_geo plot based on selected score category
    def plot_geo_map(df, selected_score):
        fig = px.scatter_geo(
            df,
            locations="Country",
            locationmode='country names',
            color=selected_score,
            size=selected_score,
            hover_name="Country",
            range_color=[df[selected_score].min(), df[selected_score].max()],
            projection="natural earth",
            color_continuous_scale="portland_r",
        )
        title_world=f'AI {selected_score} Across the Globe'
        st.markdown(f"<h2 style='font-size: 30px;'>{title_world}</h2>", unsafe_allow_html=True)
        fig.update_layout(
            showlegend=True,
            width=500,
            height=529,
            autosize=False,
            margin=dict(t=40, b=0, l=5, r=5),
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)
    if "Country" in df.columns:
        plot_geo_map(df, selected_score)

    #Sunburst Chart 
    st.markdown("""
    <div style="display: flex;">
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<h6 style='font-size: 30px;'>Region - Cluster - Income Group</h6>", unsafe_allow_html=True)
    agg_data = df[['Region', 'Cluster', 'Income group']].groupby(['Region', 'Cluster', 'Income group']).size().reset_index(name='Count')
    path = ['Region', 'Cluster', 'Income group']
    fig = px.sunburst(agg_data, values='Count', path=path, color="Region", height=585,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )  
    st.plotly_chart(fig, use_container_width=True)

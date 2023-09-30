import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline

import io

st.set_page_config(page_title="Data Exploration", page_icon = ":books:", layout="wide")

st.title(" :books: THE AI GLOBAL INDEX")
st.markdown('<style>div.block-container{padding-top:1rm;}<style>', unsafe_allow_html=True)

df = pd.read_csv("C:\\Users\Lara\Downloads\Streamlit\AI_index_db.csv")
st.subheader("Top 5 Countries")
st.write(df.head())

st.subheader("Top 5 Lowest Countries")
st.write(df.tail())

st.subheader("DataFrame Information")
buffer = io.StringIO()
df.info(buf=buffer)
# Display the captured output using st.write()
st.text(buffer.getvalue())
st.write(df.describe())

st.subheader("Column Names")
st.write(df.columns)
st.subheader("Checking the number of rows and columns and if it has a null value")
st.write("Row and Column")
st.write(df.shape)
st.write("Is there a null value in the data?")
st.write(df.isnull().values.any())
st.write("How many null value is there?")
st.write(df.isnull().values.sum())

st.subheader("Express EDA of Numeric Variables")
st.subheader("Univariate Analysis: Numerical Variables")
fig = make_subplots(rows=2, cols=4, subplot_titles=('<b>Distribution of Talent</b>',
                                                    '<b>Distribution of Infrastructure</b>',
                                                    '<b>Distribution of Operating Environment</b>',
                                                    '<b>Distribution of Research</b>',
                                                    '<b>Distribution of Development</b>',
                                                    '<b>Distribution of Government Strategy</b>',
                                                    '<b>Distribution of Commercial</b>',
                                                    '<b>Distribution of Total score</b>'
                                                   ))

fig.add_trace(go.Histogram(x=df['Talent'], nbinsx=30), row=1, col=1)
fig.add_trace(go.Histogram(x=df['Infrastructure']), row=1, col=2)
fig.add_trace(go.Histogram(x=df['Operating Environment'], nbinsx=30), row=1, col=3)
fig.add_trace(go.Histogram(x=df['Research'], nbinsx=30), row=1, col=4)
fig.add_trace(go.Histogram(x=df['Development'], nbinsx=30), row=2, col=1)
fig.add_trace(go.Histogram(x=df['Government Strategy']), row=2, col=2)
fig.add_trace(go.Histogram(x=df['Commercial'], nbinsx=30), row=2, col=3)
fig.add_trace(go.Histogram(x=df['Total score'], nbinsx=30), row=2, col=4)

                                
# Update visual layout
fig.update_layout(
    showlegend=False,
    width=950,
    height=500,
    autosize=False,
    margin=dict(t=15, b=0, l=5, r=5),
    template="plotly_white",
)

fig.update_annotations(font_size=10)
st.plotly_chart(fig)

st.subheader("Number of Countries by Region")
dfg = df['Region'].value_counts().reset_index()
dfg.columns = ['Region', 'Quantity']
f = px.bar(dfg, x='Region', y='Quantity', 
             title='Number of Countries in Report by Region (Continent)') 
st.plotly_chart(f)











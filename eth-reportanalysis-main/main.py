import pandas as pd
import plotly.express as px
import numpy as np
import altair as alt
from io import StringIO
import streamlit as st

uploaded_files = st.file_uploader("Choose a .rmon file",type = ['csv','rmon'], key=None)

#ethrmon.plotrmon('BW Util', uploaded_files)
def plotrmon(filepath):
        dataframe = pd.read_csv(filepath, sep = ","
                , skiprows=1)
        if dataframe.dtypes["RX Octs"] == np.object:
                dataframe["RX Octs"] = dataframe["RX Octs"].str.replace(r'\D', '',regex=True).astype(float)     
        if dataframe.dtypes["TX Octs"] == np.object:
           dataframe["TX Octs"] = dataframe["TX Octs"].str.replace(r'\D', '',regex=True).astype(float)
        dataframe["Bandwidth RX"] = dataframe["RX Octs"].apply(
                                                        lambda x :(x*8/900)/1e6)
        dataframe["Bandwidth TX"] = dataframe["TX Octs"].apply(
                                                        lambda x :(x*8/900)/1e6)
        df = dataframe[["Time Stamp","Bandwidth TX", "Bandwidth RX"]]
        df = pd.melt(df, id_vars = "Time Stamp", 
                         value_vars = ["Bandwidth RX", "Bandwidth TX"], 
                                                     var_name = 'BW Type')
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['GameWeek'], empty='none')
        chart = alt.Chart(df, title = "Bandwidth").mark_line().encode(
                alt.X("Time Stamp"),
                    y=alt.Y("value", stack=None, title = "Bandwidth"),
                        color="BW Type:N").properties(
                                    width = 1080, height = 480)   
        bandwidth = st.number_input(label="Input Bandwidth :")
        col1, col2, col3,col4 = st.columns(4)
        col1.metric('Max RX',round(dataframe["Bandwidth RX"].max(),2),delta=None)
        col2.metric('Max TX',round(dataframe["Bandwidth TX"].max(),2),delta=None)
        col3.metric('Bandwidth TX Util (%)', (lambda x : round(x/bandwidth*100,2) if bandwidth > 0 else None)(dataframe["Bandwidth TX"].max()),delta=None)
        col4.metric('Bandwidth RX Util (%)', (lambda x : round(x/bandwidth*100,2) if bandwidth > 0 else None)(dataframe["Bandwidth RX"].max()),delta=None)
        return st.altair_chart(chart) 
if uploaded_files is not None:
          # To read file as bytes:
     bytes_data = uploaded_files.getvalue()
     #st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_files.getvalue().decode("utf-8"))
     #st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     #st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
     plotrmon(uploaded_files)
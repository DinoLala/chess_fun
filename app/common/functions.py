import requests
from bs4 import BeautifulSoup
import pandas as pd

import streamlit as st

def get_entry_list(tourname_name):
    # Upload CSV file
    # uploaded_file = st.file_uploader("/Users/trangnguyen/Downloads/entry_list_test.csv", type="csv")
    uploaded_file = "/Users/trangnguyen/Downloads/entry_list_test.csv"

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file, index_col=0)
        df['Player'] = df['Player'].apply(lambda x: f'<a href="https://www.uschess.org/msa/MbrDtlMain.php?30581110" target="_blank">{x}</a>')

        # Display the DataFrame with hyperlinks
        table_style = """
        <style>
        .dataframe {
            width: 500px;  /* Adjust width of the table */
            margin-left: auto;
            margin-right: auto;
        }
        th {
            text-align: left;  /* Center the header text */
        }
        td {
            text-align: left;  /* Optional: center-align table data cells */
        }
        </style>
            """
        # Display the styled table with hyperlinks
        st.markdown(table_style, unsafe_allow_html=True)
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

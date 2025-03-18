import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle 

from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_all_games
from app.common.functions import get_entry_list,get_pairing

import streamlit as st

import requests


st.set_page_config(layout="wide")
import streamlit as st
tourname_name="2025 George O'Rourke Memorial"


def main():
    st.title("Wachusset Chess club tournament")
    
    # Create tabs
    tab1, tab2, tab3,tab4, tab5 = st.tabs(["Home", "Entry List", 'Pairing','Standing',"Grandpix Table"])
    
    with tab1:
        st.header("Home Page")
    
    with tab2:
        # st.header("Entry list")
        # st.write("This is where analytics data will be displayed.")

        # Title of the Streamlit app
        tourname_name="2025 George O'Rourke Memorial"
        st.title(f"Ratings in effect for the {tourname_name}:")
        get_entry_list(tourname_name)

        


    with tab4:
        st.title(f"{tourname_name} ")
        st.subheader(f":orange[ Standing- Example]")

        # Upload CSV file
        # uploaded_file = st.file_uploader("/Users/trangnguyen/Downloads/entry_list_test.csv", type="csv")
        uploaded_file = "/Users/trangnguyen/Downloads/standing_example.csv"

        if uploaded_file is not None:
            # Read the uploaded CSV file into a DataFrame
            df = pd.read_csv(uploaded_file)
            df = df.fillna('')

            # df=df[['Bd','Res','White','Res.1','Black']]
            # df = df.fillna('9999999')

            # df['Bd']=df['Bd'].astype('int')
            # df=df.replace('9999999','').replace(9999999,'')
            # df['Bd']=df['Bd'].astype('str')
            # df['Player'] = df['Player'].apply(lambda x: f'<a href="https://www.uschess.org/msa/MbrDtlMain.php?30581110" target="_blank">{x}</a>')
            
            # Display the DataFrame with hyperlinks
            table_style = """
            <style>
            .dataframe {
                width: 800px;  /* Adjust width of the table */
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
                    

    with tab3:
        st.header("Pairing Round 3 ")
        TABLE_STYLE = """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    text-align: center;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
                button {
                    padding: 5px 10px;
                    font-size: 14px;
                }
            </style>
        """
        tourname_name="2025 George O'Rourke Memorial"
        section='open'
        # Inject custom CSS
        st.markdown(TABLE_STYLE, unsafe_allow_html=True)
        st.subheader("OPEN SECTION")

        with st.expander("Click to expand"):
            get_pairing(tourname_name,section)
            
        st.subheader("U1600 SECTION")
        section='u1600'

        with st.expander("Click to expand"):
            get_pairing(tourname_name,section)
            st.write("**Enter Result**")
            


    with tab5:
        
        st.write('test')
        # Sample pairing table data




        
if __name__ == "__main__":
    main()

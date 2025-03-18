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
from app.common.functions import get_entry_list,get_pairing,get_standing

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
        section='open'
        st.subheader(f":orange[ Standing- Section: {section} Example]")

        with st.expander("Click to expand"):
            get_standing(tourname_name, 'open')
        

        
                    

    with tab3:
        st.header("Pairing Round 3 ")
        
        tourname_name="2025 George O'Rourke Memorial"
        section_option = st.selectbox("Choose section:", ["open", "u1600"])
        uploaded_file ="/Users/trangnguyen/Downloads/pairing_all.csv"
        df_all = pd.read_csv(uploaded_file)
        df_all=df_all[['section','round','Bd','Res','White','Res.1','Black']]
        
        df_all = df_all.fillna('9999999')

        df_all['Bd']=df_all['Bd'].astype('int')
        df_all=df_all.replace('9999999','').replace(9999999,'')

        df=df_all.loc[(df_all['section']==section_option)]
        last_round=df_all['round'].max()
        df=df.loc[df['round']==last_round]


        st.write(f"You selected: {section_option}")

        # section='open'

        # Inject custom CSS
        # st.subheader("OPEN SECTION")

        # with st.expander("Click to expand"):
        #     get_pairing( tourname_name,section)
        #     if st.button("Save Result 1"):
        #         st.session_state.result1 = 1
        #         st.success("Result 1 saved!")


        st.subheader(f"{section_option} SECTION")
        # section='u1600'

        with st.expander("Click to expand"):
            get_pairing( df,tourname_name,section_option)


    with tab5:
        
        st.write('TBD')
        # Sample pairing table data




        
if __name__ == "__main__":
    main()

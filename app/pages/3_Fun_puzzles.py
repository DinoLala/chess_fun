import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st


import requests

st.set_page_config(layout="wide")

st.header(':orange[Have fun solving puzzles with us !]')

col1, col2 = st.columns(2,gap="medium")
with col1:
    # st.image("app/data/chess2.png")
    st.write(':blue[White to move and draw]')
    st.image("app/data/puzzles/1.png")

    
with col2:

    # st.header(":orange[PLAYER LOOK UP]")
    # st.title(":orange[!!!]")
    # st.title(":orange[Never gonna give you up, Never gonna let you down!!!]")
    # st.title(":orange[Happy player!!!]")
    st.write(':blue[White to move and win]')
    st.image("app/data/puzzles/2.png")
   
col1, col2 = st.columns(2,gap="medium") 
with col1:
    # st.image("app/data/chess2.png")

    st.write(':blue[White to move and win]')
    st.image("app/data/puzzles/3.png")

    
with col2:

    # st.header(":orange[PLAYER LOOK UP]")
    # st.title(":orange[!!!]")
    # st.title(":orange[Never gonna give you up, Never gonna let you down!!!]")
    # st.title(":orange[Happy player!!!]")
   
    st.write(':blue[White to move and win]')
    st.image("app/data/puzzles/4.png")

            

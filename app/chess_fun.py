import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd


import streamlit as st


# st.subheader('For more information, please visit US Chess official website')
col1, col2=st.columns(2)
with col1:
    st.header(':orange[Having Fun with Chess!!]')
   
with col2:
    st.image('./app/data/nhan.jpeg')

url = "https://new.uschess.org/"
# st.write("check out this [link](%s)" % url)
st.write(":orange[For more information, please visit US Chess official [website ](%s)]" % url)

maca_tournament = "http://www.masschess.org/Events/chess-event-calendar.aspx"
continental_tour="http://www.chesstour.com/refs.html"
Duy_chess_note='https://docs.google.com/spreadsheets/d/10Lfybi_B-zMD2yyJdxc6Kos1qRIaEHC5dDKvz3OZJwU/edit?gid=0#gid=0'
st.write(":orange[For MACA [Tournaments ](%s)]" % maca_tournament)
st.write(":orange[For Continental Chess Association [Tournaments ](%s)]" % continental_tour)
st.write(":orange[Duy Chess note [note ](%s)]" % Duy_chess_note)
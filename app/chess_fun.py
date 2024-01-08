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
st.write(":orange[For MACA [Tournaments ](%s)]" % maca_tournament)
st.write(":orange[For Continental Chess Association [Tournaments ](%s)]" % continental_tour)
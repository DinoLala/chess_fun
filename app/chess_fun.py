import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd


import streamlit as st
st.header(':orange[Having Fun with Chess!!]')

# st.subheader('For more information, please visit US Chess official website')

url = "https://new.uschess.org/"
# st.write("check out this [link](%s)" % url)
st.subheader(":orange[For more information, please visit US Chess official [website ](%s)]" % url)

import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
from app.common.search import process_html, get_player,get_tournaments,get_norm_summary
import streamlit as st


st.set_page_config(layout="wide")

st.sidebar.header(':orange[USCF Norms sytem:]' )
st.sidebar.write('* Rating 2400: Life Senior Master (S)' )
st.sidebar.write('* Rating 2200: Life Master (M) ' )
st.sidebar.write('* Rating 2000 Candidate Master (C) ' )
st.sidebar.write('* Rating 1800: 1st Category (1)' )
st.sidebar.write('* Rating 1600: 2nd Category (2)' )
st.sidebar.write('* Rating 1400: 3rd Category (3)' )
st.sidebar.write('* Rating 1200: 4th Category (4)' )


col1, col2 = st.columns(2)
with col1:

    st.image("app/data/chess.png")
    # st.image("app/data/chess2.png")
    uscf_id=st.text_input('USCF_ID' ,value='')
    
with col2:

    # st.header(":orange[PLAYER LOOK UP]")
    # st.title(":orange[!!!]")
    # st.title(":orange[Never gonna give you up, Never gonna let you down!!!]")
    st.title(":orange[Happy player!!!]")

    # st.title(":orange[This is for my beloved son. Have Funs !!!]")
    col11, col21,col23 = st.columns(3)
    # with col21 :
    #     st.image("app/data/happy-dance-excited.gif")
    

h=process_html()
# try:
#     uscf_id=str(int(uscf_id))
# except: 
#     uscf_id='12743305'

submited=st.button('Find player')
url = "https://new.uschess.org/players/search"
# st.write("check out this [link](%s)" % url)
st.write(":orange[Visit [website ](%s) for official player rating look up]" % url)

if submited and uscf_id !="":

    st.divider() 
    st.header(":orange[Player Summary !]")
    # st.markdown(
    #     ":orange[Player Summary !]"
    # )

    with st.container():
        # st.write("This is inside the container")
        col1, col2, col3 = st.columns(3)
        

        dict_out=get_player(h,uscf_id)
        # dict_out['Name']=Name
        # dict_out['State']=State
        # dict_out['Gender']=Gender
        # dict_out['Junior_Ranking']=Junior_Ranking
            # dict_out['Junior_Ranking']=Junior_Ranking
        # dict_out['Over_Ranking']=Over_Ranking
        # dict_out['State_Ranking']=State_Ranking
        # dict_out['title_name']=title_name
        # dict_out['current_rating']=current_rating

        with col1:
            #    st.header("A cat")
            st.write(dict_out['Name'])
            # st.write('Gender:',dict_out['Gender'])
            st.write('State:',dict_out['State'])
            st.write('Current Title:',dict_out['title_name'])

            
            
            
            #    st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            #    st.header("A dog")
            # st.write('State:',dict_out['State'])
            
            st.write('Current USCF Rating:', dict_out['current_rating'])
            st.write('Next month USCF Rating:', dict_out['nextmonth_rate'])
            
            #    st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            #    st.header("An owl")
            st.write('Overall Ranking:', dict_out['Over_Ranking'])
            st.write('State Ranking:', dict_out['State_Ranking'])
            st.write('Junior Ranking:', dict_out['Junior_Ranking'])


    norm_df=get_norm_summary(h,uscf_id)
    st.write(':orange[Lastest Norm:]')
    if len(norm_df)==0:
        st.write('This player has no norm yet!')
    else:
        norm_df=norm_df.sort_values(by=['level'])
        st.dataframe(norm_df.tail(1))
    # st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.divider() 

    # st.write('Lastest Tournaments:':orange[orange])

    st.header(":orange[Lastest Tournaments!]")
    # st.markdown(
    #     ":orange[Lastest Tournaments !]"
    # )



    html_tables=get_tournaments(h,uscf_id)
    st.dataframe(html_tables, width=1600, height=300)


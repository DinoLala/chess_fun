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
import streamlit as st

import requests


st.set_page_config(layout="wide")

st.sidebar.header(':orange[USCF Norms sytem:]' )
st.sidebar.write('* Rating 2400: Life Senior Master (S)' )
st.sidebar.write('* Rating 2200: Life Master (M) ' )
st.sidebar.write('* Rating 2000 Candidate Master (C) ' )
st.sidebar.write('* Rating 1800: 1st Category (1)' )
st.sidebar.write('* Rating 1600: 2nd Category (2)' )
st.sidebar.write('* Rating 1400: 3rd Category (3)' )
st.sidebar.write('* Rating 1200: 4th Category (4)' )

h=process_html()

col10, col20= st.columns(2)
# favorite players ----
import json 
json_file_path = 'app/data/common_players.json'

with open(json_file_path, 'r') as j:
    df_common_players = json.loads(j.read())

favor_list=df_common_players.keys()
# load recent games 


    
with col10:

    st.image("app/data/chess.png")

    
    common_list=[ c for c in df_common_players.keys() if c !='DUY TUONG NGUYEN'] 
    common_list.sort()
    common_list.insert(0,'DUY TUONG NGUYEN')
    # common_list.insert(0,'none')
    # for idx, row in df_common_players.items():
    col1, col2= st.columns(2)
    with col1:
        # common_player = st.selectbox( 'Favor Player?',common_list)
        player_to_plot=st.multiselect(
    "Select three players:",
    common_list,
    max_selections=5,
)
        uscf_id_list=[]
        for p in player_to_plot:
            uscf_id=df_common_players[p]
            uscf_id_list.append([uscf_id,p])
            
    
with col20:

    st.title(":orange[Happy player!!!]")
    st.title("")


# st.write(uscf_id_list)

submited=st.button('Compare players')

def get_data_uscfID(uscf_id):
    df_all_games=pd.read_csv('app/data/players/allgames'+uscf_id+'.csv')
    html_tables=pd.read_csv('app/data/players/tournament'+uscf_id+'.csv')
 
    html_tables=html_tables.sort_values(by='End_event_date', ascending=True)
    # print('-----',html_tables.dtypes)
    html_tables['reg Rtg Before/After']=html_tables['reg Rtg Before/After'].astype(str)
    df_temp=html_tables.loc[~html_tables['reg Rtg Before/After'].str.contains("ONL")]
    # print(df_temp)

    df_temp['rating']=df_temp['reg Rtg Before/After'].apply(lambda x: x.split('=>')[-1].split('(')[0] if "ONL" not in x else '')
    
    # df_temp['quick_rating']=df_temp['Quick Rtg Before/After'].apply(lambda x: x.split('=>')[-1].split('(')[0] if "ONL" not in x else '')
    
    df_temp=df_temp[['rating','End_event_date']].copy().dropna()
    # df_temp_quick=html_tables[['End_event_date','quick_rating']].copy()

    df_temp=df_temp.loc[(df_temp['rating']!=' ') ]
    df_temp=df_temp.loc[(df_temp['rating']!='') ]
    df_temp=df_temp.loc[~df_temp['rating'].str.contains("nan")]

    df_temp['rating']=df_temp['rating'].astype('int')
    df_temp.index=df_temp['End_event_date']
    df_temp['y_m']=df_temp['End_event_date'].apply(lambda x: x[:7])
    # df_temp2=df_temp.groupby('y_m').agg(avg_rating=('rating','mean')).reset_index()
    df_temp2=df_temp.groupby('y_m').agg(avg_rating=('rating','last')).reset_index()

    
    df_temp2['avg_rating']=round(df_temp2['avg_rating'])
    df_temp2=df_temp2.sort_values(by='y_m', ascending=True)

    return df_temp2



if submited :


    # df_all_games=pd.read_csv('app/data/players/allgames'+uscf_id+'.csv')
    # html_tables=pd.read_csv('app/data/players/tournament'+uscf_id+'.csv')
    # st.write(html_tables)
    # st.write('plot')

    color=['orange']
    try:
        
        two_subplot_fig = plt.figure(figsize=(16,10),facecolor='lightblue')


        plt.subplot(211)
        cnt=0
        
        for id,p in uscf_id_list:
            df_temp=get_data_uscfID(id)
            
            
            cnt=cnt+1
            if cnt==1:
                df_temp_plot=df_temp
                x_stick=[df_temp_plot['y_m'][i] for i  in range(len(df_temp_plot['y_m'])) if i%3 == 0 ]
                plt.plot(df_temp_plot['y_m'] ,df_temp_plot['avg_rating'] ,  marker='.', label=p)
            else:
            
                df_temp_plot=df_temp.merge(df_temp_plot, how='inner', on='y_m', suffixes=('_'+p,''))
                
                plt.plot(df_temp_plot['y_m'] ,df_temp_plot['avg_rating'+'_'+p] ,  marker='.', label=p)
                
                


            


        plt.xticks(rotation=30)
        
        plt.xticks(x_stick)
        plt.grid()
        plt.legend()
        plt.title('Rating trend')
        st.pyplot(two_subplot_fig)
        df_temp_plot=df_temp_plot.rename(columns={'avg_rating':'avg_rating_'+uscf_id_list[0][1]})
        
        st.write(df_temp_plot.sort_values(by='y_m', ascending=False))
        

    except:
        pass



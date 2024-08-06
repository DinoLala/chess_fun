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
    common_list.insert(0,'none')
    # for idx, row in df_common_players.items():
    col1, col2= st.columns(2)
    with col1:
        common_player = st.selectbox( 'Favor Player?',common_list)
        if common_player =='none':
            uscf_id=st.text_input('USCF_ID' ,value='')
        else:
            uscf_id=df_common_players[common_player]
        more_tour_info=st.selectbox('More info' ,['none','recent tournaments', 'recent games'])
        refresh_info=st.selectbox('Update infor(* not recommend)' ,['no','yes'])
        game_num=st.selectbox(' Games stats' ,['10','20','30','50','100'])
    
with col20:

    st.title(":orange[Happy player!!!]")
    st.title("")




submited=st.button('Find player')
# url = "https://new.uschess.org/players/search"
url='http://www.uschess.org/msa/MbrDtlMain.php?'+uscf_id
# st.write("check out this [link](%s)" % url)
st.write(":orange[Visit [website ](%s) for official player rating look up]" % url)

if submited and uscf_id !="":
    if refresh_info =='yes' :
        for p in favor_list:
        # for p in ["SARAH NGUYEN"]:
            # if p !='none':
            # if p =="SARAH NGUYEN":
            uscf_id=df_common_players[p]
            df_all_games=get_all_games(uscf_id)
            # print('================checking')
            # print(df_all_games)
            html_tables=get_tournaments(h,uscf_id)
            df_all_games.to_csv('app/data/players/allgames'+uscf_id+'.csv')
            html_tables.to_csv('app/data/players/tournament'+uscf_id+'.csv')

            dict_out=get_player(h,uscf_id)
            norm_df=get_norm_summary(h,uscf_id)
            norm_df.to_csv('app/data/players/norm'+uscf_id+'.csv')
            # dict_out.to_csv('app/data/players/norm'+uscf_id+'.csv')
            

            with open('app/data/players/meta_dict'+uscf_id+'.pkl', 'wb') as f:
                pickle.dump(dict_out, f)
                    
            




    st.divider() 
    st.header(":orange[Player Summary !]")

    with st.container():
        col1, col2, col3 = st.columns(3)
        

        dict_out=get_player(h,uscf_id)
        with col1:

            st.write(dict_out['Name'])
            st.write('Gender:',dict_out['Gender'])
            st.write('State:',dict_out['State'])
            # if "none" not in dict_out['title_name']:
            st.write('Current Title:',dict_out['title_name'])
        with col2:
            
            st.write('Current USCF Rating:', dict_out['current_rating'])
            st.write('Next month USCF Rating:', dict_out['nextmonth_rate'])
            
            #    st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            #    st.header("An owl")
            st.write('Overall Ranking:', dict_out['Over_Ranking'])
            st.write('State Ranking:', dict_out['State_Ranking'])
            st.write('Junior Ranking:', dict_out['Junior_Ranking'])


    
    
    if common_player !='none':
        df_all_games=pd.read_csv('app/data/players/allgames'+uscf_id+'.csv')
        html_tables=pd.read_csv('app/data/players/tournament'+uscf_id+'.csv')
        with open('app/data/players/meta_dict'+uscf_id+'.pkl', 'rb') as f:
            dict_out = pickle.load(f)
        norm_df=pd.read_csv('app/data/players/norm'+uscf_id+'.csv', index_col=0)
        # print(norm_df)

    else:
        norm_df=get_norm_summary(h,uscf_id)
       
        # st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    

        html_tables=get_tournaments(h,uscf_id)
        
        df_all_games=get_all_games(uscf_id)

    st.write(':orange[Lastest Norm:]')
    if len(norm_df)==0:
        st.write('This player has no norm yet!')
    else:
        norm_df=norm_df.sort_values(by=['level'])
        norm_df.columns=['Norm','Norm count']
        st.dataframe(norm_df.tail(5))

    st.divider() 

    st.header(":orange[Lastest Games Statistis!]")
    

    print(df_all_games.columns)
    html_tables['short_event2']=html_tables['Event_name'].apply(lambda  x: x.split(':')[0][:-5].replace(' ',''))
    # st.dataframe(html_tables, width=1600, height=400)
    if len(df_all_games) >0:
        df_all_games['short_event']=df_all_games['Event'].apply(lambda  x: x.replace(' ',''))

        df_all_games=df_all_games.merge(html_tables[['short_event2','End_event_date']], how='left', left_on='short_event', right_on='short_event2')
        df_all_games=df_all_games.drop_duplicates()
        df_all_games=df_all_games[['End_event_date','Event',	'Section',	'round','color','Oponent USCF'	,'Oponent name','Rating','Result']]
        df_all_games=df_all_games.sort_values(by=['End_event_date','round'], ascending= False)
        game_num=int(game_num)
        st.write(f':orange[summary of last {game_num} regular games]')
        df_top=df_all_games.head(game_num)
        df_top['opp_rating']=df_top['Rating'].apply(lambda x: x.split('=>')[1].split('(')[0]).astype(float)
        df_top_w=df_top.loc[df_top['Result']=="W"]
        df_top_d=df_top.loc[df_top['Result']=="D"]
        df_top_l=df_top.loc[df_top['Result']=="L"]
        df_w=pd.DataFrame(df_top_w['opp_rating'].describe()).rename(columns={'opp_rating':'Win'})
        df_d=pd.DataFrame(df_top_d['opp_rating'].describe()).rename(columns={'opp_rating':'Draw'})
        df_l=pd.DataFrame(df_top_l['opp_rating'].describe()).rename(columns={'opp_rating':'Lose'})
        df_summary=pd.concat( [df_w,df_d,df_l], axis=1)
        st.dataframe(df_summary, width=1200, height=400)
    
    if more_tour_info=='recent games':
        

        st.dataframe(df_all_games, width=1600, height=400)
    elif more_tour_info =='recent tournaments':
        st.write(":orange[Lastest Tournaments!]")
        col_keep=[c for c in list(html_tables) if 'short' not in c and "Unname" not in c]
        html_tables_out=html_tables[col_keep]
        st.dataframe(html_tables_out, width=1600, height=400)


    try:
        html_tables=html_tables.sort_values(by='End_event_date', ascending=True)
        print('-----',html_tables.dtypes)
        html_tables['reg Rtg Before/After']=html_tables['reg Rtg Before/After'].astype(str)
        df_temp=html_tables.loc[~html_tables['reg Rtg Before/After'].str.contains("ONL")]
        print(df_temp)

        df_temp['rating']=df_temp['reg Rtg Before/After'].apply(lambda x: x.split('=>')[-1].split('(')[0] if "ONL" not in x else '')
        
        # df_temp['quick_rating']=df_temp['Quick Rtg Before/After'].apply(lambda x: x.split('=>')[-1].split('(')[0] if "ONL" not in x else '')
        
        df_temp=df_temp[['rating','End_event_date']].copy().dropna()
        # df_temp_quick=html_tables[['End_event_date','quick_rating']].copy()

        df_temp=df_temp.loc[(df_temp['rating']!=' ') ]
        df_temp=df_temp.loc[(df_temp['rating']!='') ]
        df_temp=df_temp.loc[~df_temp['rating'].str.contains("nan")]
        # print('========================')
        # print(df_temp)
        # print('========================')

        df_temp['rating']=df_temp['rating'].astype('int')
        df_temp.index=df_temp['End_event_date']

    except:
        print('----------ERRROR ')
        pass



    with col20:

        # How to set the graph size 
        
        try:
            two_subplot_fig = plt.figure(figsize=(6,6),facecolor='lightblue')
            plt.subplot(211)
            plt.plot(df_temp['End_event_date'] ,df_temp['rating'] , color='tab:orange', marker='.')
            # plt.subplot(212)
            # plt.plot(df_temp['End_event_date'] ,df_temp['quick_rating'] , color='tab:blue', marker='.')
            plt.xticks(rotation=30)
            x_stick=[df_temp['End_event_date'][i] for i  in range(len(df_temp['End_event_date'])) if i%5 == 0 ]
            plt.xticks(x_stick)
            plt.grid()
            plt.title('Rating trend')
            st.pyplot(two_subplot_fig)

        except:
            pass



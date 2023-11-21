import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary
import streamlit as st

import requests


class process_html(object):
    def read_text(self, html_file):
        text_file=open(html_file,"r")
        html_str=text_file.read()
        text_file.close()
        return html_str
    def process_tb(self, html_str):
        # soup=BeautifulSoup(html_str,'html.parse')
        soup = BeautifulSoup(html_str, "lxml")
        tables=[
            [
                [
                    td.get_text(strip=True) for td in tr.find_all('td')
                ]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]
        if tables[-1]==[]:
            tables.pop(-1)
        df=pd.DataFrame(tables[-1][:])
        # df=df.rename(columns=df.iloc[0])
       
        df=df.iloc[1:,:]
        return df
    def get_norm_stat(self, html_str):

        soup = BeautifulSoup(html_str, "lxml")
        soup.find_all('table')
        tables=[
            [
                [
                    td.get_text(strip=True) for td in tr.find_all('td')
                ]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]
        # tables
        for t in tables:
            if t[0]==['Norms Earned Since 1991']:
                norm_tb=[tb for tb in t if len(tb)==3]

        norm_df=pd.DataFrame(norm_tb, columns=['event','section','level'])
        norm_df_sum=norm_df['level'].value_counts().reset_index()
        # norm_tb=pd.DataFrame()
        print(norm_df_sum)
        # if tables[-1]==[]:
        #     tables.pop(-1)
        # df=pd.DataFrame(tables[-1][:])
        # print(df)
        return norm_df_sum
# h=process_html()
def get_player(h, uscf_id):

    # ='30305579'
    my_url='https://www.uschess.org/msa/MbrDtlMain.php?'+uscf_id

    re = requests.get(my_url)
    dict_out={}
    # print(re.text)
    text_file=re.text
    # text_file=[c.lower() for c in text_file]
    html_tables=h.process_tb(text_file)
    col_index=html_tables[0]


    name_find=text_file.split('<b>')
    Name=[c for c in name_find if uscf_id in c][0].split('</b>')[0]
    Name=Name.split(':')[-1]
    
    State=html_tables.loc[html_tables[0]=='State',:][1].reset_index()[1][0]

    Gender=html_tables.loc[html_tables[0]=='Gender',:][1].reset_index()[1][0]
    try:
        Junior_Ranking=html_tables.loc[html_tables[0]=='Junior Ranking',:][2].reset_index()[2][0]
    except:
        Junior_Ranking='none'
    try:
        Over_Ranking=html_tables.loc[html_tables[0]=='Overall Ranking',:][2].reset_index()[2][0]
    except:
        Over_Ranking='none'

    
    try:
        # state_rank='State Ranking ('+str(State)+')'
        state_rank=[c for c in col_index if 'State Ranking' in c  and 'National' not in c][0]
        State_Ranking=html_tables.loc[html_tables[0]==state_rank,:][2].reset_index()[2][0]
    except:
        State_Ranking='none'

    try:
        title=[c for c in col_index if 'US Chess Titles Earned' in c ][0]
        # title

        title_name=html_tables.loc[html_tables[0]==title,:][1].reset_index()[1][0]
    except:
        title_name='none'

    try:
        current_rating=[c for c in col_index if 'Regular Rating' in c ][0]
        # current_rating

        current_rate=html_tables.loc[html_tables[0]==current_rating,:][1].reset_index()[1][0]
        nextmonth_rate=html_tables.loc[html_tables[0]==current_rating,:][2].reset_index()[2][0][:4]
        if len(current_rate)>4 and "Unrate" not in current_rate:
            current_rate=current_rate[:4]
        # current_rate
    except:
        current_rate='Unrate'  
        nextmonth_rate='Unrate'  
    



    title_name
    dict_out['Name']=Name
    dict_out['State']=State
    dict_out['Gender']=Gender
    dict_out['Junior_Ranking']=Junior_Ranking
    dict_out['Over_Ranking']=Over_Ranking
    dict_out['State_Ranking']=State_Ranking
    dict_out['title_name']=title_name
    dict_out['current_rating']=current_rate
    dict_out['nextmonth_rate']=nextmonth_rate

    return dict_out

def get_tournaments(h,uscf_id):
    my_url='https://www.uschess.org/msa/MbrDtlTnmtHst.php?'+uscf_id
    re = requests.get(my_url)
    # print(re.text)
    text_file=re.text
    html_tables=h.process_tb(text_file)
    if len(html_tables) <=50:
        html_tables.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
    else: 
        html_tables=html_tables.iloc[1:,:]
        
        html_tables.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
        
    html_tables['End_event_date'] =html_tables['End_event_date'].apply(lambda x: x[:10])
    return html_tables
    

def get_norm_summary(h,uscf_id):
    norm_url='https://www.uschess.org/datapage/norms-list.php?'+uscf_id
    re = requests.get(norm_url)
    text_file=re.text
    try:
        norm_df=h.get_norm_stat(text_file)
    except:
        norm_df=pd.DataFrame()

    return norm_df

def get_norm(opponent_list,n_win):
    norm_dict={}
    for c in [1200, 1400,1600,1800]:
        C_t=0
        for p in opponent_list:
            del_i=c-p
            if del_i <= -400:
                c_i=0
            elif del_i <=0 and del_i >-400:
                c_i=.5+del_i/800
            elif del_i >0 and del_i <=200:
                c_i=.5+del_i/400
            else:
                c_i=1
            C_t=C_t+c_i
        if n_win- C_t>1:
            norm_dict[c]='yes'
        else:
            norm_dict[c]='no'
    return norm_dict

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


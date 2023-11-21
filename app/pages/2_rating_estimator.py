import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
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


st.set_page_config(layout="centered")

st.sidebar.header(':orange[USCF Norms sytem:]' )
st.sidebar.write('* Rating 2400: Life Senior Master' )
st.sidebar.write('* Rating 2200: Life Master ' )
st.sidebar.write('* Rating 2000 Candidate Master (C) ' )
st.sidebar.write('* Rating 1800: 1st Category (1)' )
st.sidebar.write('* Rating 1600: 2nd Category (2)' )
st.sidebar.write('* Rating 1400: 3rd Category (3)' )
st.sidebar.write('* Rating 1200: 4th Category (4)' )



st.subheader(':orange[Estimating your post tournament rating:]' )

url = "http://www.glicko.net/ratings/approx.pdf"
# st.write("check out this [link](%s)" % url)
st.write(":orange[Visit [website ](%s) for rating estimation formula]" % url)


# n_win=st.number_input('your pointstest',min_value=0, max_value=3,step=.5)
with st.container():
    # st.write("This is inside the container")
    col1, col2, col3 = st.columns(3)
    with col1:
        current_rating=st.number_input('Your current rating',min_value=.00, max_value=3000.01, )
    with col2:
        n_prior=st.number_input(' #Prior games',min_value=.00, max_value=3000.01,value=50.0,step=1.0 )   
    
    st.divider() 
    st.write(':orange[Tournament result:]' )
    col1, col2, col3 = st.columns(3)
    with col1:
        # current_rating=st.number_input('Your current rating',min_value=.00, max_value=3000.01, )
        tour_rounds=st.number_input('#Tournament games',min_value=.00, max_value=20.01, step=1.0 )
        # tour_rounds=int(tour_rounds)
    with col2:   
        n_win=st.number_input('Your points',min_value=0.0, max_value=tour_rounds,step=.5)
   

    st.write(':orange[Your opponents rating:]' )
    col1, col2, col3 = st.columns(3)
    opponent_list=[]
    with col1:
        #    st.header("A cat")
        
        for r in range(int(tour_rounds/3)+1):
            if r*3+1 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+1),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)


    with col2:
        for r in range(int(tour_rounds/3)+1):
            if r*3+2 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+2),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)
        

    with col3:
        for r in range(int(tour_rounds/3)):
            if r*3+3 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+3),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)
    
    est_submit=st.button('Est Post Rating')
    st.divider() 
    if est_submit:
        
        if current_rating >=2355:
            N_e=n_prior
        elif current_rating >0 and current_rating <2355:
            N_e=min(50/pow(.662+ 0.00000739*pow(2569 - current_rating,2),.5),n_prior)
        else:
            current_rating =0
            N_e=0
        m=tour_rounds
        K=800/(N_e+m)
        S=n_win
        E=0
        for p in opponent_list:
            e_p=1/(1+pow(10,-(current_rating-p)/400))
            E=E+e_p
        # get Bonus B
        if tour_rounds <3:
            B=0
        else:
            temp=K*(S-E)
            temp2=14*pow(max(m,4),.5)
            B= max(0, temp-temp2)

        final_est_post=int(current_rating+K*(S-E)+B)
        # avg_opp=sum(opponent_list)/len(opponent_list)
        # post_est=(N*int(current_rating)+sum(opponent_list)+(2*n_win-tour_rounds)*400)/(N+tour_rounds)

        # st.write(avg_opp,post_est,tour_rounds)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f'Winning expectation: :orange[{round(E,2)}    ] ')
            if B>0:
                st.write(f'Expected bonus points: :orange[{int(B)}    ] ')
        with col2:    
            norm_dict=get_norm(opponent_list,n_win)
            max_norm=0
            for k, t in norm_dict.items():
                
                if t=='yes' and max_norm <k:
                    max_norm=k
                
            if max_norm>0:
                st.write(f'Expected norm {max_norm}: :orange[{norm_dict[max_norm]}]')

        
        st.header(f'Your estimated post tournament rating is :orange[{final_est_post}    ] ')

        


        st.divider() 


            

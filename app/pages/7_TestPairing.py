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

        # Upload CSV file
        # uploaded_file = st.file_uploader("/Users/trangnguyen/Downloads/entry_list_test.csv", type="csv")
        uploaded_file = "/Users/trangnguyen/Downloads/entry_list_test.csv"

        if uploaded_file is not None:
            # Read the uploaded CSV file into a DataFrame
            df = pd.read_csv(uploaded_file, index_col=0)
            df['Player'] = df['Player'].apply(lambda x: f'<a href="https://www.uschess.org/msa/MbrDtlMain.php?30581110" target="_blank">{x}</a>')

            # Display the DataFrame with hyperlinks
            table_style = """
            <style>
            .dataframe {
                width: 500px;  /* Adjust width of the table */
                margin-left: auto;
                margin-right: auto;
            }
            th {
                text-align: left;  /* Center the header text */
            }
            td {
                text-align: left;  /* Optional: center-align table data cells */
            }
            </style>
             """
            # Display the styled table with hyperlinks
            st.markdown(table_style, unsafe_allow_html=True)
            st.markdown(df.to_html(escape=False), unsafe_allow_html=True)


    with tab4:
        st.title(f"{tourname_name} ")
        st.subheader(f":orange[ Standing- Example]")

        # Upload CSV file
        # uploaded_file = st.file_uploader("/Users/trangnguyen/Downloads/entry_list_test.csv", type="csv")
        uploaded_file = "/Users/trangnguyen/Downloads/standing_example.csv"

        if uploaded_file is not None:
            # Read the uploaded CSV file into a DataFrame
            df = pd.read_csv(uploaded_file)
            df = df.fillna('')

            # df=df[['Bd','Res','White','Res.1','Black']]
            # df = df.fillna('9999999')

            # df['Bd']=df['Bd'].astype('int')
            # df=df.replace('9999999','').replace(9999999,'')
            # df['Bd']=df['Bd'].astype('str')
            # df['Player'] = df['Player'].apply(lambda x: f'<a href="https://www.uschess.org/msa/MbrDtlMain.php?30581110" target="_blank">{x}</a>')
            
            # Display the DataFrame with hyperlinks
            table_style = """
            <style>
            .dataframe {
                width: 800px;  /* Adjust width of the table */
                margin-left: auto;
                margin-right: auto;
            }
            th {
                text-align: left;  /* Center the header text */
            }
            td {
                text-align: left;  /* Optional: center-align table data cells */
            }
            </style>
             """
            # Display the styled table with hyperlinks
            st.markdown(table_style, unsafe_allow_html=True)
            st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
                    

    with tab3:
        st.header("Pairing Round 3 ")
        TABLE_STYLE = """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    text-align: center;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
                button {
                    padding: 5px 10px;
                    font-size: 14px;
                }
            </style>
        """

        # Inject custom CSS
        st.markdown(TABLE_STYLE, unsafe_allow_html=True)
        uploaded_file = "/Users/trangnguyen/Downloads/pairing_example.csv"
        df = pd.read_csv(uploaded_file)
        df=df[['Bd','Res','White','Res.1','Black']]
        df = df.fillna('9999999')

        df['Bd']=df['Bd'].astype('int')
        df=df.replace('9999999','').replace(9999999,'')

        # Store table in session state to persist updates
        if "pairing_table" not in st.session_state:
            st.session_state.pairing_table = df.copy()

        if "selected_row" not in st.session_state:
            st.session_state.selected_row = None  # To track which row's button was clicked

        # Display the pairing table
        st.subheader("Pairing Table")
        table_html = """<table><tr><th>Bd</th>
                        <th>Res</th>
                        <th>White</th>
                        <th>Res.1</th>
                        <th>Black</th>
                        <th>Enter Result</th>
                        </tr>"""

        # Table layout
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1,2,1])

        with col1:
            st.write("**Bd**")
        with col2:
            st.write("**res**")
        with col3:
            st.write("**Player1**")
        with col4:
            st.write("**res.1**")
        with col5:
            st.write("**player2**")
        with col6:
            st.write("**Enter Result**")
        

        # Iterate through the rows and add input fields & buttons
        for index, row in st.session_state.pairing_table.iterrows():
            # st.write(row)
            
            col1, col2, col3, col4,col5,col6= st.columns([1, 1, 2, 1,2, 1])
            
            with col1:
                st.write(row["Bd"])
            with col2:
                st.write(row["Res"])
            with col3:
                st.write(row["White"])
            with col4:
                st.write(row["Res.1"])
            with col5:
                st.write(row["Black"])
            # with col3:
            #     st.write(row["Match Result"] if row["Match Result"] else "No Result")
            
            with col6:
                if st.button(f"Enter Result", key=f"btn_{index}"):
                    st.session_state.selected_row = index  # Store selected row index

        # Open modal when a row is selected
        if st.session_state.selected_row is not None:
            with st.popover(f"Enter Result for {st.session_state.pairing_table.at[st.session_state.selected_row, 'White']} vs {st.session_state.pairing_table.at[st.session_state.selected_row, 'Black']}"):
                new_result = st.text_input("Enter Match Result:", key="result_input")

                if st.button("Save Result"):
                    # Update the result in session state
                    if new_result!='.5':
                        st.session_state.pairing_table.at[st.session_state.selected_row, "Res"] = str(new_result)
                        st.session_state.pairing_table.at[st.session_state.selected_row, "Res.1"] = str(1-int(new_result))
                    else:
                        st.session_state.pairing_table.at[st.session_state.selected_row, "Res"] = '.5'
                        st.session_state.pairing_table.at[st.session_state.selected_row, "Res.1"] = ".5"

                    if st.session_state.pairing_table.at[st.session_state.selected_row, "Black"]=='BYE':
                        st.session_state.pairing_table.at[st.session_state.selected_row, "Res.1"] = ''

                    
                    tb=st.session_state.pairing_table.at[st.session_state.selected_row, "Bd"] 
                    df.loc[df['Bd'] == tb, 'Res'] = str(new_result)
                    df.loc[df['Bd'] == tb, 'Res.1'] = str(1-int(new_result))
                    st.write(df.loc[df['Bd'] == tb])
                    df.to_csv(uploaded_file)
                    # st.write(df)

                    st.session_state.selected_row = None  # Close modal
                    st.experimental_rerun()  # Rerun app to update table

        


    with tab5:
        
        st.write('test')
        # Sample pairing table data




        
if __name__ == "__main__":
    main()

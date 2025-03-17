# import streamlit as st
# import pandas as pd

# # Title
# st.title("Pairing Table (Column View) with Save Functionality")

# # Sample pairing data
# data = {
#     'Player 1': ['Alice', 'Bob', 'Charlie'],
#     'Player 2': ['Dave', 'Eve', 'Frank'],
#     'Match Result': ['', '', '']  # Empty results initially
# }

# # Store the table in session state
# if "pairing_table" not in st.session_state:
#     st.session_state.pairing_table = pd.DataFrame(data)

# if "selected_row" not in st.session_state:
#     st.session_state.selected_row = None  # Track selected row index

# if "new_result" not in st.session_state:
#     st.session_state.new_result = ""  # Store entered result

# # Custom CSS for styling
# st.markdown(
#     """
#     <style>
#     .column-box {
#         border: 1px solid #ddd;
#         padding: 10px;
#         text-align: center;
#         background-color: #f9f9f9;
#         border-radius: 5px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Create three columns for Player 1, Player 2, and Match Result
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.subheader("Player 1")
#     for player in st.session_state.pairing_table["Player 1"]:
#         st.markdown(f'<div class="column-box">{player}</div>', unsafe_allow_html=True)

# with col2:
#     st.subheader("Player 2")
#     for player in st.session_state.pairing_table["Player 2"]:
#         st.markdown(f'<div class="column-box">{player}</div>', unsafe_allow_html=True)

# with col3:
#     st.subheader("Match Result")
#     for result in st.session_state.pairing_table["Match Result"]:
#         st.markdown(f'<div class="column-box">{result if result else "No Result"}</div>', unsafe_allow_html=True)

# with col4:
#     st.subheader("Enter Result")
#     for index in range(len(st.session_state.pairing_table)):
#         if st.button("Enter", key=f"btn_{index}"):
#             st.session_state.selected_row = index  # Store selected row index

# # Show modal when a row is selected
# if st.session_state.selected_row is not None:
#     selected_index = st.session_state.selected_row
#     player1 = st.session_state.pairing_table.at[selected_index, "Player 1"]
#     player2 = st.session_state.pairing_table.at[selected_index, "Player 2"]

#     with st.modal("Enter Match Result", key="modal"):
#         st.subheader(f"Enter Result for {player1} vs {player2}")

#         # Input field for the result
#         new_result = st.text_input("Match Result:", value=st.session_state.new_result, key="result_input")

#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Save Result"):
#                 # Save entered result into session state
#                 st.session_state.pairing_table.at[selected_index, "Match Result"] = new_result
#                 st.session_state.selected_row = None  # Close modal
#                 st.experimental_rerun()  # Refresh app to show updated results

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.selected_row = None  # Close modal
#                 st.experimental_rerun()  # Refresh app

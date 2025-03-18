import streamlit as st

st.header("Using st.modal")

# Create a button to trigger the modal
if st.button("Open Modal"):
    with st.modal("Modal Title"):
        st.write("This is a modal pop-up window.")
        st.button("Close")  # You can add an interactive close button

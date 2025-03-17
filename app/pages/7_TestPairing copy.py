import streamlit as st

st.header("Expandable Section")

with st.expander("Click to expand"):
    st.write("This content is hidden by default. Click the header to reveal it.")
    st.image("https://via.placeholder.com/150", caption="Example Image")

import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Player": ["Alice", "Bob", "Charlie"],
    "Score": [10, 20, 15],
    "Rank": [1, 2, 3]
}
df = pd.DataFrame(data)

# Convert the DataFrame to HTML and apply styling
styled_table = df.to_html(index=False)

# Custom CSS for header color (orange)
styled_table = styled_table.replace(
    '<thead>',
    '<thead style="background-color: orange; color: white;">'
)

# Display the styled table
st.markdown(styled_table, unsafe_allow_html=True)

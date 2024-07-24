import streamlit as st
import pandas as pd

# File uploader widget
uploaded_file = st.file_uploader("Choose an EXCEL file", type="xlsx")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_xlsx(uploaded_file)

sheet_names = df.sheet_names

for sheet in len(sheet_names)
    st.write(sheet)


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import streamlit as st
from streamlit_option_menu import option_menu
from login import (login)

from pages import (
    json_converter_multiple,
    generate_exams,
    json_converter,
    home
)

if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
if 'user' not in st.session_state:
        st.session_state.user = None

if st.session_state.authenticated:
    user = st.session_state.user
    st.success(f"Welcome, {user['username']}! You are logged in as a {user['role']}.")

    with st.sidebar:
        selected = option_menu(
            menu_title = "Menu",
            options = ["Home", "Exam Generator", "JSON Converter", "Multiple JSON Converter"],
            icons = ["house"],
            menu_icon="heart-eyes-fill",
            default_index=0,
        )

    if selected == "Home":
        home()

    if selected == "Exam Generator":
        generate_exams()

    if selected == "JSON Converter":
        json_converter()

    if selected == "Multiple JSON Converter":
        json_converter_multiple()

    

else:
     login()


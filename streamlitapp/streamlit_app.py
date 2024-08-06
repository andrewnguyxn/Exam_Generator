import streamlit as st
from streamlit_option_menu import option_menu
from login import (login, create_user)
from db import initialize_db
from db import create_connection, get_user, add_user, initialize_db

from pages import (
    generate_exams,
    json_converter,
    home
)

conn = create_connection('users.db')
initialize_db(conn)
conn.close()

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
            options = ["Home", "Exam Generator", "JSON Converter"],
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

    

else:
     login()


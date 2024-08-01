import streamlit as st
from streamlit_option_menu import option_menu

from pages import (
    generate_exams,
    json_converter,
    home
)

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



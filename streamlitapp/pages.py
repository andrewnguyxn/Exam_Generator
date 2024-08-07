import streamlit as st
import pandas as pd
import zipfile
import streamlit_ext as ste
import json
import re
import os
from mitosheet.streamlit.v1 import spreadsheet
from io import BytesIO
from streamlit_option_menu import option_menu

from utils import (
    generator,
    excel_to_json
)

def generate_exams():
    st.title("Generate Exams")

    uploaded_file = st.file_uploader("Upload an EXCEL file to get started", type="xlsx")

    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []

    if uploaded_file is not None:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        if st.checkbox("Edit file"):
            data = pd.read_excel(excel_file)
            spreadsheet(data)

        number_of_questions = {}
        for name in sheet_names:
            with st.expander(name):
                selected_number = st.number_input(f"Please enter the number of questions from {name}: ", min_value=0, max_value=10000, step=1)
                number_of_questions[name] = selected_number

        number_of_exams = st.number_input("How many exams do you want to generate?", min_value=1, max_value=100, step=1)
        
        if st.button('Generate'):
            st.session_state.generated_files = []

            for count in range(number_of_exams):
                output_file, df_combined = generator(uploaded_file, number_of_questions)

                json_output = excel_to_json(df_combined)

                st.session_state.generated_files.append((output_file,json_output, df_combined, f"Generated exam number {count + 1}:"))
                
            mem_zip = BytesIO()
            with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                for id, (output_file,json_output, df_combined, message) in enumerate(st.session_state.generated_files):
                    with st.expander(message):
                        st.write(df_combined)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        ste.download_button(
                            label="Download",
                            data=output_file,
                            file_name=f'exam_{id + 1}.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            #key=f'download_{id}'
                        )

                    with col2:
                        ste.download_button(
                            label="Download JSON",
                            data=json_output,
                            file_name=f'exam_{id + 1}.json',
                            mime='application/json'
                    )
                    zf.writestr(f'exam_{id + 1}.xlsx', output_file.getvalue())
                    zf.writestr(f'exam_{id + 1}.json', json_output)
        
                mem_zip.seek(0)

            ste.download_button(
                label="Download All as ZIP",
                data=mem_zip.getvalue(),
                file_name='exams.zip',
                mime='application/zip',
                #key="download_all"
            )
            
        #st.write(st.session_state)
    else:
        st.session_state.generated_files = []

# JSON Converter
def json_converter():
    st.title("Convert EXCEL file to JSON")

    uploaded_file_convert = st.file_uploader("Upload an EXCEL file to get started", type="xlsx")

    if uploaded_file_convert is not None:
        st.session_state.converted_files = []
        excel_file = pd.ExcelFile(uploaded_file_convert)
        sheet_names = excel_file.sheet_names

        for name in sheet_names:
            data = pd.read_excel(uploaded_file_convert, sheet_name=name)
            json_output = excel_to_json(data)
            st.session_state.converted_files.append((json_output, name))

        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for id, (json_output, name) in enumerate(st.session_state.converted_files):
                ste.download_button(
                    label=f"Download {name}",
                    data=json_output.encode('utf-8'),
                    file_name=f'{name}.json',
                    mime='application/json',
                )
                zf.writestr(f'{name}.json', json_output)
        
        mem_zip.seek(0)

        ste.download_button(
            label="Download All as ZIP",
            data=mem_zip.getvalue(),
            file_name='jsonfiles.zip',
            mime='application/zip',
        )

        #st.write(st.session_state)
    else:
        st.session_state.converted_files = []

def json_converter_multiple():
    st.title("Convert multiple EXCEL files to JSON")

    uploaded_files = st.file_uploader("Choose EXCEL files", type="xlsx", accept_multiple_files=True)

    if uploaded_files:
        st.write(f"You have uploaded {len(uploaded_files)} files.")
        st.session_state.converted_files_multiple = []

        if st.button("Convert to JSON"):
            for file in uploaded_files:
                excel_file = pd.ExcelFile(file)
                sheet_names = excel_file.sheet_names

                converted_files = []
                for name in sheet_names:
                    data = pd.read_excel(file, sheet_name=name)
                    json_output = excel_to_json(data)
                    converted_files.append((json_output, name))
                file_name = file.name.rsplit('.', 1)[0]
                st.session_state.converted_files_multiple.append((converted_files, file_name))

            for converted_files, file_name in st.session_state.converted_files_multiple:
                st.write(f"Download options for {file_name}:")
                mem_zip = BytesIO()
                with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for json_output, sheet_name in converted_files:
                        json_filename = f'{sheet_name}.json'
                        ste.download_button(
                            label=f"Download {json_filename}",
                            data=json_output.encode('utf-8'),
                            file_name=json_filename,
                            mime='application/json'
                        )
                        zf.writestr(json_filename, json_output.encode('utf-8'))
                mem_zip.seek(0)

                ste.download_button(
                    label=f"Download All as ZIP for {file_name}",
                    data=mem_zip.getvalue(),
                    file_name=f'{file_name}.zip',
                    mime='application/zip'
                )


                


    

# Function for home page
def home():
    st.title("Welcome to the App")
    st.write("Use the menu to navigate to different functions.")


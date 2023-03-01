import io
import requests
import streamlit as st
from pathlib import Path
from random import randint
from urls import CONVERT

def encode_files(files, url):

    multiple_files = [
        ("files", (file.name, file, file.type)) for file in files
    ]

    return requests.post(url, files=multiple_files)


def intro():
    import streamlit as st

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Whisperer is a small open-source project for text-audio auto dataset maker
        for your Machine Learning and Data Science projects.

        The Design of this WebApp is based on the available commands of the whisperer_ml package.

        **👈 Select a command from the dropdown on the left** 
    """
    )

def convert():
    db = Path("../data/raw_files")

    if 'key' not in st.session_state:
        st.session_state.key = str(randint(1000, 100000000))

    # a button to upload files
    st.title("Whisperer Dataset Maker")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, key=st.session_state.key)

    if st.button("Upload Files"):
        if uploaded_files and 'key' in st.session_state.keys():
            response = encode_files(uploaded_files, url=CONVERT)
            st.session_state.pop('key')
            st.experimental_rerun()

    if list(db.iterdir()):
        st.write("Files in Database")
        for file in db.iterdir():
            st.write(file.name)

    if st.button("Clear Files"):
        for file in db.iterdir():
            file.unlink()
        st.experimental_rerun()

    # if st.button()

page_names_to_funcs = {
    "-": intro,
    "convert": convert
}

demo_name = st.sidebar.selectbox("Choose a command", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
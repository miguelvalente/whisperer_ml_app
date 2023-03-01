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
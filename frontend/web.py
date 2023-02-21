import io
import requests
import streamlit as st
from pathlib import Path


backend = "http://localhost:8000/convertfiles"

db = Path("../data/raw_files")

def encode_files(files, url):

    multiple_files = [
        ("files", (file.name, file, file.type)) for file in files
    ]

    return requests.post(url, files=multiple_files)


# a button to upload files
st.title("Whisperer Dataset Maker")
uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

if st.button("Upload Files"):
    if uploaded_files:
        response = encode_files(uploaded_files, backend)
        # for file in uploaded_files:
        #     response = encode_files(file, backend)
        st.write(response.text)
        # st.write(f"Converting {file.name}...")

st.title("Whisperer Dataset Maker")
for file in db.iterdir():
    st.write(file)

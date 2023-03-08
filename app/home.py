import requests
import soundfile as sf
from whisperer_ml.converter import convert
from stqdm import stqdm

import pandas as pd
import streamlit as st
from random import randint

from db_paths import DB_RAW, DB_CONVERTED, DB_SPEAKERS
from format_functions import is_plural

# region SetUp Page
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.set_page_config(
    page_title="Whisperer",
    page_icon="👂",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
            # Whisperer 👂
            #### text-audio dataset-maker
    """
)

st.markdown(
    """
    Whisperer is a small open-source project for automatic text-audio dataset making.

    1. 👇 **Upload your audio files or video files to convert them to wav** 

    """
)
# endregion

if "key" not in st.session_state:
    st.session_state.key = str(randint(1000, 100000000))

# region Upload/Convert Files
uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True,
    key=st.session_state.key,
    label_visibility="hidden",
)

if st.button("Upload & Convert"):
    if uploaded_files and "key" in st.session_state.keys():
        for file in uploaded_files:
            data, samplerate = sf.read(file)
            sf.write(DB_RAW.joinpath(file.name), data, samplerate)
        st.session_state.pop("key")
        st.experimental_rerun()

raw_files = pd.DataFrame(list(DB_RAW.iterdir()), columns=["file_path"])
raw_files["filename"] = raw_files["file_path"].apply(lambda x: x.name)
for file in stqdm(raw_files["file_path"], desc="Converting files to wav..."):
    convert(raw_files["file_path"], DB_CONVERTED)
    file.unlink()
# endregion

# region Display Files
st.markdown(""" #### Your Files """)
with st.expander("Original 🎧"):
    col1, col2 = st.columns(2, gap="small")
    raw_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
    raw_files["filename"] = raw_files["file_path"].apply(lambda x: x.name)
    raw_files["delete"] = False
    if raw_files.empty:
        st.write("You have no files yet.")
    else:
        col1.dataframe(raw_files["filename"], use_container_width=True)
        user_input_raw = col2.experimental_data_editor(raw_files["delete"])
        if st.button("Delete"):
            to_delete = raw_files[user_input_raw]
            for file_path in to_delete["file_path"]:
                file_path.unlink()
            st.experimental_rerun()
# endregion

st.markdown(
    """
    2. 👈  **You have the option to diarize and to auto-label the uploaded files** 

        Navigate to the respective page to do so.
    """
)

st.markdown(
    """
    3. 🎉 **Navigate to the Transcribe page to transcribe**

        Wait for whisperer to finish the transcription and then download the dataset. 
    """
)

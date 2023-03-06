import requests
import soundfile as sf
from whisperer_ml.converter import convert
from stqdm import stqdm

import pandas as pd
import streamlit as st
from random import randint

from db_paths import DB_RAW, DB_CONVERTED
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


    1. **Upload some audio or video files**

    """
)
# endregion

if "key" not in st.session_state:
    st.session_state.key = str(randint(1000, 100000000))

# region Upload Files
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

if not raw_files.empty:
    st.markdown(
        f"""
            You have uploaded __{len(raw_files)}__ file{is_plural(len(raw_files))}
        """
    )
    st.dataframe(raw_files["filename"])
    for file in stqdm(raw_files["file_path"], desc="Converting files to wav..."):
        convert([file], DB_CONVERTED)
        file.unlink()
# endregion

st.markdown(
    """
    2. 👈  **Use the commands from the menu on the left** 
    """
)

import requests
import soundfile as sf
from whisperer_ml.converter import convert
from stqdm import stqdm

import pandas as pd
import streamlit as st
from random import randint

from db_paths import DB_RAW, DB_CONVERTED
from format_functions import is_plural

# This is Very Important always add apropiate emojis to your markdown
st.set_page_config(
    page_title="Whisperer",
    page_icon="👂",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
            # Whisperer 👂
            #### text-audio dataset-maker
    """
)

st.sidebar.success("Select a command above.")

st.markdown(
    """
    Whisperer is a small open-source project for automatic text-audio dataset making.


    1. **Upload some audio or video files**

    """
)

if "key" not in st.session_state:
    st.session_state.key = str(randint(1000, 100000000))

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

# convert_bar = st.progress(0, text="Converting files to wav...")

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

    # if st.button("Clear Files"):
    #     for file in DB_RAW.iterdir():
    #         file.unlink()
    #     st.experimental_rerun()

st.markdown(
    """
    2. 👈  **Select a command from the dropdown menu on the left** 
    """
)

import pandas as pd
# import streamlit as st
from whisperer_ml.diarizer import diarize
from db_paths import DB_CONVERTED, DB_SPEAKERS
from format_functions import is_plural


st.markdown(
    """
            # Diarize 🗣

            In this page you can diarize the diles converted to wav
            and see the diarizations you have already made.
    """
)

converted_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
converted_files["file_name"] = converted_files["file_path"].apply(lambda x: x.name)

if not converted_files.empty:
    st.markdown(
        f"""
            You have __{len(converted_files)}__ files to diarize
        """
    )
    st.dataframe(converted_files["file_name"])
else:
    st.markdown(
        f"""
            You have no file{is_plural(len(converted_files))} to diarize
        """
    )

if st.button("Diarize"):
    diarize(converted_files["file_path"], DB_SPEAKERS, join_speaker=True)

speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
speaker_files["file_name"] = speaker_files["file_path"].apply(lambda x: x.name)

if not speaker_files.empty:
    st.markdown(
        f"""
            You have __{len(speaker_files)}__ diarizations
        """
    )
    st.dataframe(speaker_files["file_name"])
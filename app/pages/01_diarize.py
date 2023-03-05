import pandas as pd
import streamlit as st
from whisperer_ml.diarizer import diarize
from db_paths import DB_CONVERTED, DB_SPEAKERS
from format_functions import is_plural

# This is Very Important always add apropiate emojis to your markdown
st.set_page_config(
    page_title="Diarize",
    page_icon="🗣",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
            # Diarize 🗣

            In this page you can diarize the diles converted to wav
            and see the diarizations you have already made.
    """
)

speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)

diarized = speaker_files["filename"].apply(
    lambda x: "_".join(x.split("_")[:-2]) + "." + x.split(".")[-1]
)

converted_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
converted_files["filename"] = converted_files["file_path"].apply(lambda x: x.name)

if not converted_files.empty:
    if len(diarized) > 0:
        converted_files = converted_files[
            ~converted_files["filename"].isin(diarized.to_list())
        ]
    if not converted_files.empty:
        st.markdown(
            f"""
                You have __{len(converted_files)}__ files to diarize
            """
        )
        st.dataframe(converted_files["filename"])
        if st.button("Diarize"):
            diarize(converted_files["file_path"], DB_SPEAKERS, join_speaker=True)
            st.experimental_rerun()
    else:
        st.markdown(
            """
                You have no files to diarize
            """
        )
else:
    st.markdown(
        f"""
            You have no file{is_plural(len(converted_files))} to diarize
        """
    )


if not speaker_files.empty:
    st.markdown(
        f"""
            You have __{len(speaker_files)}__ diarizations
        """
    )
    st.dataframe(speaker_files["filename"])

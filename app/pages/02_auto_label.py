import streamlit as st
import pandas as pd 
from db_paths import DB_SPEAKERS, DB_SPEAKERS_LABELS
from whisperer_ml.auto_labeler import auto_label

st.set_page_config(
    page_title="Auto-Label",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
            # Auto-Label 🤖

            If you diarized your files you can use this page to
            automatically find the same speakers across the diarizations

            __NOTE__: This feature is highly dependent on the quality of the diarization
            and the quality of the audio files. Uniformity of the audio files is paramount
    """
)

speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)

st.dataframe(speaker_files["filename"])

if speaker_files.empty:
    st.markdown(
        """
            You have no files to auto-label
        """
    )
else:
    number_speakers = st.number_input("Number of speakers", min_value=2, max_value=10)

    if st.button("Auto-Label"):
        if number_speakers:
            auto_label(number_speakers, speaker_files["file_path"], DB_SPEAKERS_LABELS.joinpath("speakers.txt"))
        else:
            st.error("Must define number of speakers")

if DB_SPEAKERS_LABELS.joinpath("speakers.txt").exists():
    st.markdown(
        """
            ## Speakers
        """
    )
    st.dataframe(pd.read_csv(DB_SPEAKERS_LABELS.joinpath("speakers.txt"), sep="|"))
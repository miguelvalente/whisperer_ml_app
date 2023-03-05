import streamlit as st


st.set_page_config(
    page_title="Auto-Label",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
            # Auto-Label 🤖

            If you diarized your files you can use this page to
            automatically find the same speakers across the diarizations

            #NOTE: This feature is highly dependent on the quality of the diarization
            and the quality of the audio files. Uniformity of the audio files is paramount
    """
)

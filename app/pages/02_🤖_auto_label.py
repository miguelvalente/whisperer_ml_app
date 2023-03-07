import streamlit as st
import pandas as pd
from db_paths import DB_SPEAKERS, DB_SPEAKERS_LABELS
from whisperer_ml.auto_labeler import auto_label

from utils import get_files_ignore_hidden

# region SetUp Page
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.set_page_config(
    page_title="Auto-Label",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
            # Auto-Label 🤖

            If you diarized your files you can use this page to
            automatically find the same speakers across the diarizations

            __NOTE__: This feature is highly dependent on the quality of the diarization.
    """
)
# endregion

speaker_files = pd.DataFrame(get_files_ignore_hidden(DB_SPEAKERS), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)
speaker_files["delete"] = False

# st.dataframe(speaker_files["filename"])


with st.expander("Diarized 🗣"):
    if speaker_files.empty:
        st.markdown(
            f"""
                You have no diarized files to auto-label

                Goto the [Diarize](/02_🗣_diarize) page to diarize your files and start labelling speakers

            """
        )
    else:
        st.markdown(
            f"""
                You have __{len(speaker_files)}__ diarizations
            """
        )

        col3, col4 = st.columns(2, gap="small")
        col3.dataframe(speaker_files["filename"], use_container_width=True)
        user_input = col4.experimental_data_editor(
            speaker_files["delete"],
        )
        if st.button("Delete Selected Files"):
            to_delete = speaker_files[user_input]
            for file in to_delete["filename"]:
                DB_SPEAKERS.joinpath(file).unlink()
            st.experimental_rerun()


if not speaker_files.empty:
    st.markdown(
        """
            #### Start labelling

            Note: _The new auto-label results will overwrite the previous one_
        """
    )

    number_speakers = st.number_input("Number of speakers", min_value=2, max_value=10)

    if st.button("Auto-Label"):
        if isinstance(number_speakers, int) and number_speakers >= 2:
            with st.spinner("Auto-Labeling ..."):
                DB_SPEAKERS_LABELS.joinpath("speakers.txt").unlink(missing_ok=True)
                auto_label(
                    number_speakers,
                    speaker_files["file_path"],
                    DB_SPEAKERS_LABELS.joinpath("speakers.txt"),
                )
        else:
            st.error("Must define number of speakers bigger or equal to 2")

    with st.expander("Auto-Label Results 📊"):
        if DB_SPEAKERS_LABELS.joinpath("speakers.txt").exists():
            st.dataframe(
                pd.read_csv(
                    DB_SPEAKERS_LABELS.joinpath("speakers.txt"),
                    sep="|",
                    names=["filename", "label"],
                )
            )
        else:
            st.markdown(
                """
                    You have no auto-label results
                """
            )
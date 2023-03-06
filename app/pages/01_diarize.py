import pandas as pd
import streamlit as st
from whisperer_ml.diarizer import diarize
from db_paths import DB_CONVERTED, DB_SPEAKERS
from format_functions import is_plural

# region SetUp Page
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.set_page_config(
    page_title="Diarize",
    page_icon="🗣",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
            # Diarize 🗣

            In this page you can diarize the diles converted to wav
            and see the diarizations you have already made.

            __NOTE__: This feature is highly dependent on the uniformity of the audio files.
            If a speaker in a file is present in diferent environments, the diarization might not work as expected.
    """
)
# endregion

speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)
speaker_files["delete"] = False

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
                You have __{len(converted_files)}__ file{is_plural(len(converted_files))} to diarize
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

    col1, col2 = st.columns(2, gap="small")
    col1.dataframe(speaker_files["filename"], use_container_width=True)
    user_input = col2.experimental_data_editor(
        speaker_files["delete"],
    )
    if st.button("Delete Selected Files"):
        to_delete = speaker_files[user_input]
        for file in to_delete["filename"]:
            DB_SPEAKERS.joinpath(file).unlink()
        st.experimental_rerun()

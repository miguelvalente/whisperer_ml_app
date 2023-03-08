import pandas as pd
import streamlit as st
from whisperer_ml.diarizer import diarize
from db_paths import DB_CONVERTED, DB_SPEAKERS
from utils import is_plural, get_files_ignore_hidden

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

# region DataFrames
speaker_files = pd.DataFrame(sorted(get_files_ignore_hidden(DB_SPEAKERS)), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)
speaker_files["delete"] = False

diarized = speaker_files["filename"].apply(
    lambda x: "_".join(x.split("_")[:-2]) + "." + x.split(".")[-1]
)

converted_files = pd.DataFrame(sorted(get_files_ignore_hidden(DB_CONVERTED)), columns=["file_path"])
converted_files["filename"] = converted_files["file_path"].apply(lambda x: x.name)
converted_files["number_of_speakers"] = 0 
# endregion

with st.expander("Original 🎧"):
    if converted_files.empty:
        st.markdown(
            """
                You have no files to diarize

                Goto [Home](/) to upload your files
            """
        )
    else:
        if len(diarized) > 0:
            converted_files = converted_files[
                ~converted_files["filename"].isin(diarized.to_list())
            ]
        if converted_files.empty:
            st.markdown(
                """
                    You have no files to diarize

                    Goto [Home](/) to upload your files
                """
            )
        else:
            st.markdown(
                f"""
                    You have __{len(converted_files)}__ file{is_plural(len(converted_files))} to diarize

                    You can specify the number of speakers in each file. Or leave it blank to let the algorithm decide.
                """
            )
            col1, col2 = st.columns(2, gap="small")
            col1.dataframe(converted_files["filename"], use_container_width=True)
            user_input_number = col2.experimental_data_editor(
                converted_files["number_of_speakers"],
            )
            number_of_speakers = [number if number else None for number in user_input_number]
            if st.button("Diarize"):
                st.warning("Demo version ")
                # with st.spinner("Diarizing files..."):
                #     diarize(converted_files["file_path"], DB_SPEAKERS, join_speaker=True, num_speakers=number_of_speakers)
                #     st.experimental_rerun()


with st.expander("Diarized 🗣"):
    if not speaker_files.empty:
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
            st.warning("Demo version ")
            # to_delete = speaker_files[user_input]
            # for file in to_delete["filename"]:
            #     DB_SPEAKERS.joinpath(file).unlink()
            # st.experimental_rerun()

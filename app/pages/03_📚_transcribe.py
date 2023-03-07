import pandas as pd
import streamlit as st
from whisperer_ml.transcriber import transcribe
import shutil
from db_paths import DB_CONVERTED, DB_DATASETS, DB_ARCHIVES, DB_SPEAKERS
from format_functions import is_plural

# region SetUp Page
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.set_page_config(
    page_title="Transcribe",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
            # Make a dataset 📚

            In this page you can make a dataset from the diles converted to wav
            and see the datasets you have already made.
    """
)
# endregion

# region Display Datasets
available_datasets = pd.DataFrame(list(DB_DATASETS.iterdir()), columns=["dataset_path"])
available_datasets["dataset_name"] = available_datasets["dataset_path"].apply(
    lambda x: x.name
)

st.markdown(""" #### Your Datasets 📁 """)

if not available_datasets.empty:
    selected_dataset = st.selectbox(
        "Select a dataset to download", available_datasets["dataset_name"]
    )

    down = st.download_button(
        label="Download Dataset",
        data=DB_ARCHIVES.joinpath(f"{selected_dataset}.zip").read_bytes(),
        file_name=f"{selected_dataset}.zip",
        mime="application/zip",
    )

else:
    st.write("You have no datasets yet.")
# endregion

st.markdown(""" --- """)


# region Display Files
st.markdown(""" #### Your Files """)
with st.expander("Original 🎧"):
    # region Raw Files
    col1, col2 = st.columns(2, gap="small")
    raw_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
    raw_files["filename"] = raw_files["file_path"].apply(lambda x: x.name)
    raw_files["delete"] = False
    if raw_files.empty:
        st.write("You have no files yet.")
    else:
        col1.dataframe(raw_files["filename"], use_container_width=True)
        user_input_raw = col2.experimental_data_editor(raw_files["delete"])
        if st.button("Delete Orginal"):
            to_delete = raw_files[user_input_raw]
            for file_path in to_delete["file_path"]:
                file_path.unlink()
            st.experimental_rerun()
    # endregion

# region Speaker Files
with st.expander("Diarized 🗣"):
    speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
    speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)
    speaker_files["delete"] = False
    col3, col4 = st.columns(2, gap="small")
    if speaker_files.empty:
        st.write("You have no diarized files yet.")
    else:
        col3.dataframe(speaker_files["filename"], use_container_width=True)
        user_input_speaker = col4.experimental_data_editor(speaker_files["delete"])
        if st.button("Delete Diarized"):
            to_delete = speaker_files[user_input_speaker]
            for file_path in to_delete["file_path"]:
                file_path.unlink()
            st.experimental_rerun()
    # endregion
# endregion


st.markdown("""---""")

choice = st.radio(
    "Transcribe from full files or diarized files?",
    options=["original", "diarized"],
    # label_visibility="hidden",
)

dataset_name = st.text_input(
    "dataset name", value="my_dataset_name", label_visibility="hidden"
)

if st.button("Make Dataset"):
    dataset_path = DB_DATASETS.joinpath(dataset_name)
    wavs_path = dataset_path.joinpath("wavs")
    transcription_path = dataset_path.joinpath("transcriptions")

    if not dataset_path.exists():
        dataset_path.mkdir(exist_ok=True)
        wavs_path.mkdir(exist_ok=True)
        transcription_path.mkdir(exist_ok=True)
    else:
        st.write(f"Dataset {dataset_name} already exists at {dataset_path}")

    if choice == "original":
        with st.spinner("Transcribing..."):
            transcribe(list(DB_CONVERTED.iterdir()), wavs_path, transcription_path)
    else:
        with st.spinner("Transcribing..."):
            transcribe(list(DB_SPEAKERS.iterdir()), wavs_path, transcription_path)

    shutil.make_archive(
        DB_ARCHIVES.joinpath(dataset_name),
        "zip",
        DB_DATASETS.joinpath(dataset_name),
    )
    st.experimental_rerun()

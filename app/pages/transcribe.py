import pandas as pd
import streamlit as st
from whisperer_ml.transcriber import transcribe
import shutil
from db_paths import DB_CONVERTED, DB_DATASETS, DB_ARCHIVES, DB_SPEAKERS
from format_functions import is_plural

st.markdown(
    """
            # Make a dataset 📚

            In this page you can make a dataset from the diles converted to wav
            and see the datasets you have already made.
    """
)

available_datasets = pd.DataFrame(list(DB_DATASETS.iterdir()), columns=["dataset_path"])
available_datasets["dataset_name"] = available_datasets["dataset_path"].apply(
    lambda x: x.name
)

# Developer Note: Always add emojis to every single st.markdown but do not repeat them
st.markdown(
    """
            #### Your Datasets 📁
    """
)

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

st.markdown(
    """
            #### Transcribe your files and make a new dataset 📝
    """
)


col1, col2 = st.columns(2)

raw_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
raw_files["filename"] = raw_files["file_path"].apply(lambda x: x.name)
if not raw_files.empty:
    col1.markdown(
        f"""
            You have __{len(raw_files)}__ audio file{is_plural(len(raw_files))} to transcribe
        """
    )
    col1.dataframe(raw_files["filename"])

speaker_files = pd.DataFrame(list(DB_SPEAKERS.iterdir()), columns=["file_path"])
speaker_files["filename"] = speaker_files["file_path"].apply(lambda x: x.name)
if not speaker_files.empty:
    col2.markdown(
        f"""
            You have __{len(speaker_files)}__ diarized audio file{is_plural(len(speaker_files))} to transcribe
        """
    )
    col2.dataframe(speaker_files["filename"])

choice = st.radio(
    "Transcribe from",
    options=["regular", "diarized"],
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

    if choice == "regular":
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

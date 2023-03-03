import requests
import streamlit as st
from pathlib import Path
from random import randint

DB_RAW = Path("data/raw_files")
DB_CONVERTED = Path("data/converted_files")
DB_DATASETS = Path("data/datasets")
DB_ARCHIVES = Path("data/archives")


def make_plural(size):
    return "s" if size > 1 else ""


# This is Very Important always add apropiate emojis to your markdown
def encode_files(files, url):
    multiple_files = [("files", (file.name, file, file.type)) for file in files]

    return requests.post(url, files=multiple_files)


def intro():
    import streamlit as st
    import pandas as pd
    import soundfile as sf
    from whisperer_ml.converter import convert
    from stqdm import stqdm

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

    if st.button("Upload"):
        if uploaded_files and "key" in st.session_state.keys():
            for file in uploaded_files:
                data, samplerate = sf.read(file)
                sf.write(DB_RAW.joinpath(file.name), data, samplerate)
            st.session_state.pop("key")
            st.experimental_rerun()

    raw_files = pd.DataFrame(list(DB_RAW.iterdir()), columns=["file_path"])
    raw_files["file_name"] = raw_files["file_path"].apply(lambda x: x.name)

    # convert_bar = st.progress(0, text="Converting files to wav...")

    if not raw_files.empty:
        st.markdown(
            f"""
                You have uploaded __{len(raw_files)}__ file{make_plural(len(raw_files))}
            """
        )
        st.dataframe(raw_files["file_name"])
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

def diarize():
    import streamlit as st
    from whisperer_ml.diarizer import diarize

    st.markdown(
        """
             # Diarize 🗣

             In this page you can diarize the diles converted to wav
             and see the diarizations you have already made.
        """
    )

def transcribe():
    import streamlit as st
    from whisperer_ml.transcriber import transcribe
    import pandas as pd
    import shutil

    st.markdown(
        """
             # Make a dataset 📚

             In this page you can make a dataset from the diles converted to wav
             and see the datasets you have already made.
        """
    )

    available_datasets = pd.DataFrame(
        list(DB_DATASETS.iterdir()), columns=["dataset_path"]
    )
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

    raw_files = pd.DataFrame(list(DB_CONVERTED.iterdir()), columns=["file_path"])
    raw_files["file_name"] = raw_files["file_path"].apply(lambda x: x.name)
    if not raw_files.empty:
        st.markdown(
            f"""
                You have __{len(raw_files)}__ files to transcribe
            """
        )
        st.dataframe(raw_files["file_name"])

    dataset_name = st.text_input(
        "dataset name", value="my_dataset_name", label_visibility="hidden"
    )

    if st.button("Make"):
        dataset_path = DB_DATASETS.joinpath(dataset_name)
        wavs_path = dataset_path.joinpath("wavs")
        transcription_path = dataset_path.joinpath("transcriptions")

        if not dataset_path.exists():
            dataset_path.mkdir(exist_ok=True)
            wavs_path.mkdir(exist_ok=True)
            transcription_path.mkdir(exist_ok=True)
        else:
            st.write(f"Dataset {dataset_name} already exists at {dataset_path}")
        transcribe(list(DB_CONVERTED.iterdir()), wavs_path, transcription_path)

        shutil.make_archive(
            DB_ARCHIVES.joinpath(dataset_name),
            "zip",
            DB_DATASETS.joinpath(dataset_name),
        )
        st.experimental_rerun()


page_names_to_funcs = {
    "-": intro,
    "diarize": diarize,
    "transcribe": transcribe,
}

demo_name = st.sidebar.selectbox("Choose a command", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
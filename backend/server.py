import io
from typing import List
from fastapi import FastAPI, UploadFile, File
import wave
import soundfile as sf
from pydantic import BaseModel
from pathlib import Path

db = Path("../data/raw_files")

app = FastAPI(
    title="Whisperer Dataset Maker",
    description="A simple API for Whisperer",
    version="0.1.0",
)


@app.post("/convertfiles")
async def save_files(files: List[UploadFile]):
    for file in files:
        data, samplerate = sf.read(file.file)
        sf.write(db.joinpath(file.filename), data, samplerate)
    return {"filenames": [file.filename for file in files]}
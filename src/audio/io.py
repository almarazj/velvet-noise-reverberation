import os
import numpy as np
import soundfile as sf


def read_audio_file(file_path):
    """
    Reads a single audio file and returns its data and sampling rate.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    data, fs = sf.read(file_path)
    duration = len(data) * fs
    return {"data": data, 
            "duration": duration,
            "fs": fs
    }


def save_audio_file(audio_data: np.ndarray, sample_rate: int, path: str) -> str:
    """
    Saves the given audio data to the specified path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, audio_data, sample_rate)
    return os.path.abspath(path)

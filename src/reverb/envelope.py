import numpy as np


def envelope(signal: np.ndarray,
             sample_rate: int,
             reverberation_time: float, 
             amplitude: float=1, 
             bias: float=0.00001) -> np.ndarray:
    
    time = np.arange(len(signal)) / sample_rate
    b = 3 / (reverberation_time * np.log(np.e))
    env = amplitude * np.exp(-b * time) + bias
    
    return env * signal

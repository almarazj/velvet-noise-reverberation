import numpy as np
import pyloudnorm as pyln


def normalize(data: np.ndarray, sample_rate: int, LUFS: int=-18) -> np.ndarray:
    meter = pyln.Meter(sample_rate)
    loudness = meter.integrated_loudness(data)
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, LUFS)
    return loudness_normalized_audio


def add_gap(signal: np.ndarray, sample_rate: int, gap: int) -> np.ndarray:
    gap_samples = int(gap * sample_rate / 1000)
    signal[1:gap_samples] = 0
    return signal


def add_direct_sound(signal: np.ndarray, sample_rate: int, gap: float, target_drr: float) -> np.ndarray:
    M = len(signal)
    N = int((gap/1000) * sample_rate)   

    reverberated = np.sum(signal[N:M]**2)
    other_direct_energy = np.sum(signal[1:N]**2)
    direct_energy = reverberated * (10 ** (target_drr / 10))
    first_sample_squared = direct_energy - other_direct_energy

    signal[0] = np.sqrt(first_sample_squared)
    return signal


def generate_rir(signal: np.ndarray, sample_rate: int, gap: float, target_drr: float) -> np.ndarray:
    signal_with_gap = add_gap(signal, sample_rate, gap)
    signal_with_direct_sound = add_direct_sound(signal_with_gap, sample_rate, gap, target_drr)
    return signal_with_direct_sound

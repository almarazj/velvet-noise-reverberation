import numpy as np


def DRR(rir: np.ndarray, sample_rate: int, direct_length) -> float:
    M = len(rir)
    N = int((direct_length/1000) * sample_rate)
    h2 = rir ** 2

    direct = np.sum(h2[0:N-1])
    reverberated = np.sum(h2[N:M])

    return 10 * np.log10(direct/reverberated)

import numpy as np


def generate_velvet_noise(duration: int, 
                          sample_rate: int, 
                          pulse_density: int, 
                          ensureLast: bool = False) -> np.ndarray:
    """Generate velvet noise signal.

    Args:
        duration (int): Duration of the signal in seconds
        sample_rate (int): Sample rate of the signal
        pulse_density (int): Number of pulses per second
        ensureLast (bool, optional): Force the last pulse to occur within the last window. Defaults to False.

    Returns:
        np.ndarray: Generated velvet noise signal
    """
    duration+=1                            # More natural fade out
    N = int(duration * sample_rate)        # number of samples
    T = sample_rate / pulse_density        # pulse period
    nP = int(np.ceil(N/T))                 # number of pulses to generate
    Y = np.zeros(N)                        # output signal

    # calc pulse location (Välimäki, et al, Eq. 2 & 3)
    for m in range(nP-1):                                   # m needs to start at 0
        p_idx = round((m*T) + np.random.rand()*(T-1))       # k_m, location of pulse within this pulse period
        if p_idx <= N:                                      # make sure the last pulse is in bounds (in case nP was fractional)
            Y[p_idx+1] = (2 * round(np.random.rand()) - 1)  # value of pulse: 1 or -1
                                                            # p_idx+1: bump from 0- to 1-based indexing
        elif ensureLast == 1:
            p_idx = round((m*T) + np.random.rand()*(T-1-N%T))
            Y[p_idx+1] = round(np.random.rand()) - 1 
            print('forcing last pulse within bounds')

    return Y


def exponentia_velvet_noise(duration: int, sample_rate: int, initial_interval: float, decay_rate: float) -> np.ndarray:
    t = np.arange(0, duration, 1/sample_rate)
    signal = np.zeros_like(t)
    signal[0] = 10
    current_time = 0
    while current_time < duration:
        index = int(current_time * sample_rate + np.random.rand() * initial_interval * sample_rate  * np.exp(-decay_rate * current_time))
        if index < len(signal):
            signal[index] = 2 * round(np.random.rand()) - 1
        current_time += initial_interval * np.exp(-decay_rate * current_time)

    return signal


def generate_white_noise(duration: int, sample_rate: int) -> np.ndarray:
    return np.random.normal(0, 0.3, int(duration * sample_rate))

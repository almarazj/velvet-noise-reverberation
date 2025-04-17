import numpy as np
import librosa
from dtw import dtw
from numpy.linalg import norm
import matplotlib.pyplot as plt
from src.analytics.spectrum import smoothing

def plot_time_series(signals, fs, titles=None, filename=None, figsize=(12, 8)):
    """
    Plot multiple time series signals for comparison.
    """
    if not isinstance(signals, list):
        signals = [signals]
    
    if titles is None:
        titles = [f"Signal {i+1}" for i in range(len(signals))]
    elif len(titles) < len(signals):
        titles.extend([f"Signal {i+1}" for i in range(len(titles), len(signals))])
    
    n_plots = len(signals)
    fig, axes = plt.subplots(n_plots, 1, figsize=figsize, sharex=True)
    
    # Handle case of single plot
    if n_plots == 1:
        axes = [axes]
    
    for i, (signal, title) in enumerate(zip(signals, titles)):
        t = np.arange(len(signal)) / fs
        axes[i].plot(t, signal)
        axes[i].set_title(title)
        axes[i].set_ylabel("Amplitude")
        axes[i].grid(True, alpha=0.3)
    
    axes[-1].set_xlabel("Time (s)")
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
        print(f"Plot saved to {filename}")
    
    return fig


def plotDtw(norm_audio_gn, norm_audio_vn, fs):
    plt.subplot(1,2,1)
    mel1 = librosa.feature.melspectrogram(y=norm_audio_gn, sr=fs, n_mels=128, fmax=16000)
    S1_dB = librosa.power_to_db(mel1, ref=np.max)
    librosa.display.specshow(S1_dB)

    plt.subplot(1,2,2)
    mel2 = librosa.feature.melspectrogram(y=norm_audio_vn, sr=fs, n_mels=128, fmax=16000)
    S2_dB = librosa.power_to_db(mel2, ref=np.max)
    librosa.display.specshow(S2_dB)

    plt.show()

    dist, cost, acc_cost, path = dtw(S1_dB.T, S2_dB.T, dist=lambda x, y: norm(x - y, ord=1))
    print('Normalized distance between the two sounds:', dist)

    plt.imshow(cost.T, origin='lower', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.xlim((-0.5, cost.shape[0]-0.5))
    plt.ylim((-0.5, cost.shape[1]-0.5))
    plt.show()
    

def plotSpectrum(data1, data2):
    vA = np.fft.fft(data1)
    gA = np.fft.fft(data2)
    vX = 20*np.log10(np.abs(vA))
    gX = 20*np.log10(np.abs(gA))
    freq = np.arange(0, len(vX), 1)
    vpower_3 = smoothing(freq[20:20000], vX[20:20000], 3)
    gpower_3 = smoothing(freq[20:20000], gX[20:20000], 3)

    plt.semilogx(vpower_3, 'k')
    plt.semilogx(gpower_3, 'r')
    plt.ylim(0, 50)
    plt.xlim(20,16000)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Level [dB]')
    plt.show()
    
    
# file_path = filedialog.askopenfilename(title = "Select Audio File", filetypes = [("WAV files", "*.wav")])
# x, fs = sf.read(file_path)

# S = librosa.feature.melspectrogram(y=x, sr=fs, n_mels=128,
#                                     fmax=16000)
# fig, ax = plt.subplots(figsize=(5,3))
# S_dB = librosa.power_to_db(S, ref=np.max)
# img = librosa.display.specshow(S_dB, x_axis='time',
#                          y_axis='mel', sr=fs,
#                          fmax=16000, ax=ax)
# fig.colorbar(img, ax=ax, format='%+2.0f dB', ticks=[0, -20, -40, -60, -80])
# plt.yticks([512, 1024, 2048, 4096, 8192], ['0.5', '1', '2', '4', '8'])
# plt.ylabel('Frecuency [kHz]')
# plt.xlabel('Time [s]')
# plt.tight_layout()
# plt.subplots_adjust(left=0.11, right=0.995, top=0.98, bottom=0.15)
# plt.show()
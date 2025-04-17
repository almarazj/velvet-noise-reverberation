# Pulse density thresholds of velvet noise used in artificial reverberation

![WIP](https://img.shields.io/badge/status-work_in_progress-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/almarazj/velvet-noise-reverberation)
![License](https://img.shields.io/github/license/almarazj/velvet-noise-reverberation)

> 🚧 **This project is a work in progress.**

## 🎧 Overview

This project explores the minimum pulse density required for velvet noise to be subjectively perceived as Gaussian white noise when used in artificial reverberation. The study includes:

- Stimulus generation using synthetic RIRs
- Velvet noise with varying pulse densities
- ABX listening test procedure
- Data analysis and threshold estimation

You can find the full paper in the `paper/` folder.

## 🗂️ Project Structure

```HTML
. ├── data/       # Original and generated audio data
  ├── notebooks/  # Analysis and visualization
  ├── paper/      # Original paper in pdf
  ├── results/    # Plots and CSV results
  ├── scripts/    # Scripts to generate audio signals and plots
  ├── src/        # Source code to process audio signals
  |  ├── analytics/
  |  ├── audio/
  |  ├── reverb/
  |  └── visualization/
  ├── setup.py
  ├── LICENSE
  ├── pyproject.toml
  └── README.md
```

## ⚙️ Requirements

Dependencies are managed using poetry:

```bash
poetry install
```

```bash
eval "$(poetry env activate)"
```

## 🚀 Usage

Example to generate a test stimulus using white noise:

```bash
python scripts/generate_stimulus.py -f data/0_drum.wav -n White -v
```

Example to generate a test stimulus using velvet noise with a pulse density of 300 p/s:

```bash
python scripts/generate_stimulus.py -f data/0_drum.wav -n Velvet -pd 300 -v
```

## 📊 Reproducing Results

See `notebooks/analysis.ipynb` for data analysis and threshold plots.

import sys
import argparse
from pathlib import Path
import scipy.signal as sig
from src.audio.io import read_audio_file, save_audio_file
from src.audio.processing import normalize, generate_rir
from src.reverb.envelope import envelope
from src.reverb.noise import generate_velvet_noise, generate_white_noise
from src.visualization.plots import plot_time_series


def main():
    """Main function to parse arguments and process audio_data."""
    parser = argparse.ArgumentParser(description="Apply velvet noise reverberation to audio_data files.")
    
    parser.add_argument("-f", "--filepath", required=True, help="Input audio_data file path")
    parser.add_argument("-n", "--noise", choices=["Velvet", "White"], default="Velvet", help="Type of noise to use (default: Velvet)")
    parser.add_argument("-rt", "--reverberation-time", type=float, default=1.0, help="Reverberation time in seconds (default: 1.0)")
    parser.add_argument("-dr", "--drr", type=float, default=10.0, help="Direct-to-reverberant ratio in dB (default: -3.0)")
    parser.add_argument("-pd", "--pulse_density", type=int, default=2000, help="Velvet noise density in pulses per second (default: 2000)")
    parser.add_argument("-g", "--gap", type=int, default=9, help="Time gap before first reflection in ms (default: 9)")
    parser.add_argument("-v", "--visualize", action="store_true", help="Generate visualization plots of processing stages")

    args = parser.parse_args()
    
    input_path = Path(args.filepath)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1

    try:
        audio_data = read_audio_file(input_path)

        if args.noise == "Velvet":
            noise = generate_velvet_noise(args.reverberation_time, audio_data["fs"], args.pulse_density)
            output_path = input_path.with_name(f"{input_path.stem}_{args.pulse_density}ps{input_path.suffix}")
        elif args.noise == "White":
            noise = generate_white_noise(args.reverberation_time, audio_data["fs"])
            output_path = input_path.with_name(f"{input_path.stem}_white_noise{input_path.suffix}")

        enveloped_noise = envelope(noise, audio_data["fs"], args.reverberation_time)

        rir = generate_rir(enveloped_noise, audio_data["fs"], args.gap, args.drr)

        reverberated_signal = sig.convolve(audio_data["data"], rir)

        normalized_reverberated_signal = normalize(reverberated_signal, audio_data["fs"])

        save_audio_file(normalized_reverberated_signal, audio_data["fs"], output_path)
        
        if args.visualize:
            plots_dir = Path("results/plots")
            plots_dir.mkdir(exist_ok=True)

            signals = [audio_data["data"], noise, rir, normalized_reverberated_signal]
            titles = ["Input Audio", f"{args.noise} noise", "Artificial RIR", "Reverberated Signal"]
            plot_time_series(signals, audio_data["fs"], titles, plots_dir / f"{input_path.stem}.png", figsize=(12, 10))            

    except Exception as e:
        print(f"Error processing audio_data: {e}", file=sys.stderr)
        return 1

    print("Processing complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())

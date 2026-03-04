from tools.wav_decoder import wav_to_json
from tools.downloader import download
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to the encoded *.wav file.")
parser.add_argument("-o", "--output", default="decoded_banana.png", type=str, help="Path to output the decoded *.png file.")

def main():
    args = parser.parse_args()
    data = wav_to_json(args.input)
    download(data, args.output)
    print(f"Success! File is saved to: {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
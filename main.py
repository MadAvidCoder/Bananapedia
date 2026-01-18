from tools.wav_decoder import wav_to_json
from tools.downloader import download

data = wav_to_json('encoded.wav')
download(data, 'decoded_banana.png')
print("Success! File is saved to: decoded_banana.png")
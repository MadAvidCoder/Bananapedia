import json
import wave
import struct

with open("../revisions.txt", "r") as f:
    revisions = [l.strip() for l in f.readlines()]

with open("../metadata.json", "r") as f:
    meta = json.load(f)

meta['revisions'] = revisions

raw = json.dumps(meta).encode('utf-8')

samples = []
for b in raw:
    sample = (b - 128) * 16 ## 0-255 to -32768–32767
    samples.append(sample)

with wave.open("../encoded.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(8000)
    for s in samples:
        f.writeframes(struct.pack('<h', s))
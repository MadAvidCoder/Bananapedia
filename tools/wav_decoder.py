import json
import struct
import wave

def wav_to_json(file):
    with wave.open(file, 'r') as f:
        frames = f.readframes(f.getnframes())

    samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)
    raw = bytes((s // 256 + 128) & 0xFF for s in samples)

    return json.loads(raw.decode("utf-8"))
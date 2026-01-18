import json
import struct
import wave

def wav_to_json(file):
    with wave.open(file, 'r') as f:
        if f.getsampwidth() != 2:
            raise ValueError("Expected 16-bit PCM")
        if f.getnchannels() != 1:
            raise ValueError("Expected mono audio")

        frames = f.readframes(f.getnframes())

    samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)

    raw_bytes = bytes(
        max(0, min(255, (s // 16) + 128))
        for s in samples
    )

    return json.loads(raw_bytes.decode("utf-8"))
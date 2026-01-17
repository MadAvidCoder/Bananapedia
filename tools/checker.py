from fetcher import get_sentences
from decoder import decode
import json


with open("../encoded.json", "r") as f:
    data = json.load(f)

bitstream = data['bitstream']
chunks = [bitstream[i:i+3] for i in range(0, len(bitstream), 3)]

with open("../revisions.txt", "r") as f:
    revisions = [s.rstrip() for s in f.readlines()]

edits = get_sentences(revisions)

fails = 0

for i, edit in enumerate(edits):
    decoded = decode(edit)
    original = chunks[i]
    if original != decoded:
        print(f"ERROR: line {i}: {original} != {decoded}")
        fails += 1

print("-------------------------------------------------")
print(f"{fails} {'error' if fails == 1 else 'errors'} out of {len(edits)} {'revision' if len(edits) == 1 else 'revisions'}")
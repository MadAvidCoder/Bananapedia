from tools.fetcher import get_sentences
from tools.decoder import decode
import json
from PIL import Image

with open("revisions.txt", "r") as f:
    revisions = [l.strip() for l in f.readlines()]

with open("metadata.json", "r") as f:
    metadata = json.load(f)

bitstream = ""

edits = get_sentences(revisions)

for edit in edits:
    bitstream += decode(edit)

width = metadata["width"]
palette = metadata["palette"]
codes = metadata["codes"]

decode_map = {v: eval(k) for k, v in codes.items()}

decoded_rle = []
code = ""
for bit in bitstream:
    code += bit
    if code in decode_map:
        decoded_rle.append(decode_map[code])
        code = ""

pixels = []
for colour, count in decoded_rle:
    pixels.extend([colour] * count)

height = len(pixels) // width
img = Image.new("P", (width, height))
img.putpalette(palette)
img.putdata(pixels[:width*height])
img = img.convert("RGB")

img.show()
img.save("decoded_banana.png")
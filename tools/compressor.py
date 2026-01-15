## A tool to assist in decreasing the overall size of the image, with quantization, RLE and huffman, and then output a binary string.

from PIL import Image
import heapq
from collections import Counter, namedtuple
import json

banana = Image.open("../banana.png").convert("RGB")
banana = banana.quantize(10)
banana = banana.resize((59, 38))

# Metadata for reconstruction
palette = banana.getpalette()
width = banana.width

RLE = []
cur_colour = -1
count = 0
for pixel in banana.get_flattened_data():
    if pixel == cur_colour:
        count += 1
        if count > 64:
            RLE.append((cur_colour, count))
            count = 0
    else:
        if count > 0:
            RLE.append((cur_colour, count))
        count = 1
        cur_colour = pixel
if count > 0:
    RLE.append((cur_colour, count))

frequencies = Counter(RLE)

# Huffman
Node = namedtuple("node", ["symbol", "freq", "left", "right"])
counter = 0
heap = []
for symbol, freq in frequencies.items():
    heapq.heappush(heap, (freq, counter, Node(symbol, freq, None, None)))
    counter +=1

while len(heap) > 1:
    f1, c1, n1 = heapq.heappop(heap)
    f2, c2, n2 = heapq.heappop(heap)
    merger= Node(None, f1 + f2, n1, n2)
    heapq.heappush(heap, (f1 + f2, counter, merger))
    counter += 1

root = heap[0][2]

huffman_encoded = {}
def encode(node, code=""):
    if node.symbol is not None:
        huffman_encoded[str(node.symbol)]  = code
    else:
        encode(node.left, code + '0')
        encode(node.right, code + '1')

encode(root)

bitstream = ""
for symbol in RLE:
    bitstream += huffman_encoded[str(symbol)]

data = {
    'bitstream': bitstream,
    'width': width,
    'palette': palette,
    'codes': huffman_encoded
}

with open("../encoded.json", "w") as f:
    json.dump(data, f)
## A helper script that reads out the chunks one at a time for easy Wikipedia editing
## It also tracks the revision ids for use later!
import json

with open("../encoded.json", "r") as f:
    data = json.load(f)

bitstream = data['bitstream']
chunks = [bitstream[i:i+3] for i in range(0, len(bitstream), 3)]

start = input("Start Chunk Index: ")
try:
    start = min(int(start), len(chunks))
except:
    start = 0

for i in range(start, len(chunks)):
    print(f"Chunk ID: {i}")
    print(chunks[i])
    print(f"Oxford Comma: {'YES' if chunks[i][0] == '1' else 'NO'}")
    print(f"Discourse Marker: {'YES' if chunks[i][1] == '1' else 'NO'}")
    print(f"Parentheses: {'YES' if chunks[i][2] == '1' else 'NO'}")
    print()
    x = input("Input Revision ID: ")
    with open("../revisions.txt", "a") as f:
        f.write(x)
        f.write("\n")
    print("-----------------------------------------------------")
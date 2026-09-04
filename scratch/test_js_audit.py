import re
import sys

with open("static/js/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in app.js: {len(lines)}")

# Find all DOM element listener declarations
unguarded = []
for idx, line in enumerate(lines, 1):
    if ".addEventListener(" in line:
        # check preceding lines or current line for guard
        prev = lines[max(0, idx-4):idx-1]
        prev_str = "".join(prev)
        target = line.split(".addEventListener")[0].strip()
        # if target is document, window, anchor, card, chip, btn, check if guarded
        print(f"L{idx}: {line.strip()}")


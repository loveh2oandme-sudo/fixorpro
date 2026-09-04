import re
from pathlib import Path

js_path = Path("static/js/app.js")
js_content = js_path.read_text(encoding="utf-8")

print(f"app.js total lines: {len(js_content.splitlines())}")

# Check element IDs referenced in app.js vs index.html
html_path = Path("static/index.html")
html_content = html_path.read_text(encoding="utf-8")

# Find all document.getElementById("...") in app.js
id_matches = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', js_content)
print(f"Unique IDs queried in app.js: {len(set(id_matches))}")

missing_ids = []
for el_id in set(id_matches):
    if f'id="{el_id}"' not in html_content and f"id='{el_id}'" not in html_content:
        missing_ids.append(el_id)

print(f"Missing IDs in index.html: {missing_ids}")

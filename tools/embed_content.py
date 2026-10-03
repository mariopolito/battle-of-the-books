"""Copy content JSON into the app's embedded <script type="application/json"> block.

Usage: python tools/embed_content.py [content/battle1-2026.json] [index.html]
Edit the JSON file, run this, then reopen the HTML. (Or edit the block in the HTML directly.)
"""
import json, pathlib, re, sys

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "content/battle1-2026.json")
app = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "index.html")

text = src.read_text(encoding="utf-8")
json.loads(text)  # fail loudly on invalid JSON
text = text.replace("</", "<\\/")  # keep the browser from ending the <script> early

html = app.read_text(encoding="utf-8")
pat = re.compile(r"(<!-- CONTENT:START -->\s*<script type=\"application/json\" id=\"bob-content\">\n).*?(\n</script>\s*<!-- CONTENT:END -->)", re.S)
if not pat.search(html):
    sys.exit("Could not find the CONTENT:START / CONTENT:END block in " + str(app))
html = pat.sub(lambda m: m.group(1) + text.rstrip("\n") + m.group(2), html, count=1)
app.write_text(html, encoding="utf-8")
print(f"Embedded {src} into {app}")

#!/usr/bin/env python3
"""Render hands-on-workshop.md into a Google Codelabs page (index.html + codelab.json).

Produces the same <google-codelab> structure as `claat export`, so either works:
    python3 scripts/export.py          # needs: pip install markdown
    claat export hands-on-workshop.md  # if you have claat installed (then copy its output to the root)
"""

import datetime as dt
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "hands-on-workshop.md"


def parse(text: str):
    head, _, body = text.partition("\n\n")
    meta = dict(line.split(":", 1) for line in head.splitlines() if ":" in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    steps, current, in_fence = [], None, False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            current = {"title": line[3:].strip(), "duration": 0, "lines": []}
            steps.append(current)
            continue
        if current is None:
            continue
        m = re.match(r"^Duration:\s*(\d+):(\d+)(?::(\d+))?\s*$", line)
        if not in_fence and m and not current["lines"]:
            h, mnt, sec = (int(x) if x else 0 for x in m.groups())
            current["duration"] = h * 60 + mnt if m.group(3) else mnt  # h:mm:ss or mm:ss
            continue
        current["lines"].append(line)
    return meta, steps


def render_step(lines: list[str]) -> str:
    out = markdown.markdown("\n".join(lines), extensions=["fenced_code", "tables"])
    # Blockquote notes -> codelab callouts
    out = re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", r'<aside class="special">\1</aside>', out, flags=re.S)
    out = out.replace("<h3>", "<h2 is-upgraded>").replace("</h3>", "</h2>")
    out = re.sub(r'<code class="language-(\w+)">', r'<code class="language-\1" translate="no">', out)
    return out


PAGE = """<!doctype html>

<html>
<head>
  <meta name="viewport" content="width=device-width, minimum-scale=1.0, initial-scale=1.0, user-scalable=yes">
  <meta name="theme-color" content="#4F7DC9">
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="//fonts.googleapis.com/css?family=Source+Code+Pro:400|Roboto:400,300,400italic,500,700|Roboto+Mono">
  <link rel="stylesheet" href="//fonts.googleapis.com/icon?family=Material+Icons">
  <link rel="stylesheet" href="https://storage.googleapis.com/claat-public/codelab-elements.css">
  <style>
    .success {{ color: #1e8e3e; }}
    .error {{ color: red; }}
    google-codelab-step img {{ max-width: 100%; border: 1px solid #e0e0e0; border-radius: 6px; }}
    google-codelab-step table {{ border-collapse: collapse; }}
    google-codelab-step th, google-codelab-step td {{ border: 1px solid #dadce0; padding: 6px 10px; vertical-align: top; }}
  </style>
</head>
<body>
  <google-codelab codelab-gaid=""
                  id="{id}"
                  title="{title}"
                  environment="web"
                  feedback-link="{feedback}">
{steps}
  </google-codelab>

  <script src="https://storage.googleapis.com/claat-public/native-shim.js"></script>
  <script src="https://storage.googleapis.com/claat-public/custom-elements.min.js"></script>
  <script src="https://storage.googleapis.com/claat-public/prettify.js"></script>
  <script src="https://storage.googleapis.com/claat-public/codelab-elements.js"></script>

</body>
</html>
"""


def main():
    meta, steps = parse(SRC.read_text())
    blocks = "\n".join(
        f'      <google-codelab-step label="{html.escape(s["title"])}" duration="{s["duration"]}">\n'
        f'{render_step(s["lines"])}\n      </google-codelab-step>\n'
        for s in steps
    )
    title = meta["title"]
    (ROOT / "index.html").write_text(PAGE.format(
        title=html.escape(title), id=meta["id"], feedback=html.escape(meta.get("feedback link", "")), steps=blocks))
    (ROOT / "codelab.json").write_text(json.dumps({
        "environment": "web", "format": "html", "id": meta["id"], "title": title, "summary": meta["summary"],
        "source": SRC.name, "status": [meta.get("status", "Published").lower()],
        "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "authors": meta.get("authors", ""), "duration": sum(s["duration"] for s in steps),
        "updated": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"), "url": meta["id"],
    }, indent=2) + "\n")
    print(f"{len(steps)} steps, {sum(s['duration'] for s in steps)} minutes -> index.html")


if __name__ == "__main__":
    main()

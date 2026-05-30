#!/usr/bin/env python3
"""Render mermaid code blocks in Markdown files to SVG and embed images.

Usage: python3 scripts/render_mermaid_to_svg.py

This script:
 - Walks through java-projects/JtProject-Next/doc
 - Finds ```mermaid``` fenced blocks
 - Renders each block to an SVG using npx @mermaid-js/mermaid-cli (mmdc)
 - Writes the SVG to an `assets/` folder next to the Markdown
 - Inserts an image reference above the mermaid block and keeps the mermaid
   block inside a collapsible details section for editability.

If npx or network is not available, the script will print instructions.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = ROOT / "java-projects" / "JtProject-Next" / "doc"

MERMAID_RE = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


def ensure_assets_dir(md_path: Path) -> Path:
    assets = md_path.parent / "assets"
    assets.mkdir(exist_ok=True)
    return assets


def render_mermaid_to_svg(mmd_content: str, out_svg: Path) -> bool:
    # create a temp input file
    tmp_mmd = out_svg.with_suffix(".mmd")
    tmp_mmd.write_text(mmd_content, encoding="utf-8")

    cmd = [
        "npx",
        "-y",
        "@mermaid-js/mermaid-cli",
        "-i",
        str(tmp_mmd),
        "-o",
        str(out_svg),
    ]
    try:
        print("Rendering mermaid to", out_svg)
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp_mmd.unlink(missing_ok=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to render:", e)
        print(e.stdout.decode() if e.stdout else "", e.stderr.decode() if e.stderr else "")
        return False


def process_file(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    matches = list(MERMAID_RE.finditer(text))
    if not matches:
        return False

    assets = ensure_assets_dir(md_path)
    new_text = []
    last_index = 0
    changed = False
    for i, m in enumerate(matches, start=1):
        start, end = m.span()
        mermaid_code = m.group(1).strip()

        # write preceding content
        new_text.append(text[last_index:start])

        # create svg filename
        base = md_path.stem
        svg_name = f"{base}-mermaid-{i}.svg"
        svg_path = assets / svg_name

        ok = render_mermaid_to_svg(mermaid_code, svg_path)
        if ok:
            # insert image reference and keep mermaid in a details block
            img_md = f"![diagram]({svg_path.relative_to(md_path.parent)})\n\n"
            details = f"<details>\n<summary>Mermaid source</summary>\n\n```mermaid\n{mermaid_code}\n```\n</details>\n\n"
            new_text.append(img_md)
            new_text.append(details)
            changed = True
        else:
            # fallback: keep original block
            new_text.append(m.group(0))

        last_index = end

    new_text.append(text[last_index:])

    if changed:
        md_path.write_text("".join(new_text), encoding="utf-8")
    return changed


def main():
    if not DOC_ROOT.exists():
        print("Doc root not found:", DOC_ROOT)
        sys.exit(1)

    md_files = list(DOC_ROOT.rglob("*.md"))
    processed = []
    for md in md_files:
        try:
            changed = process_file(md)
            if changed:
                print("Updated:", md)
                processed.append(md)
        except Exception as e:
            print("Error processing", md, e)

    print(f"Done. Processed {len(processed)} files.")


if __name__ == "__main__":
    main()

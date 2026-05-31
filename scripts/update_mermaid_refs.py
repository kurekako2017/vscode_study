#!/usr/bin/env python3
"""Update Markdown files to reference generated .mmd/.svg assets for mermaid blocks.

This script:
 - Walks java-projects/JtProject-Next/doc for Markdown files
 - For each ```mermaid``` block it writes the mermaid source to assets/{md-stem}-mermaid-{n}.mmd
 - If an SVG with the same base exists, it inserts an image reference; otherwise
   it inserts a link to the .mmd file.
 - The original mermaid source is preserved inside a collapsible <details> block.

Usage: python3 scripts/update_mermaid_refs.py
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = ROOT / "java-projects" / "JtProject-Next" / "doc"

MERMAID_RE = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


def ensure_assets_dir(md_path: Path) -> Path:
    assets = md_path.parent / "assets"
    assets.mkdir(exist_ok=True)
    return assets


def process_file(md_path: Path) -> bool:
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

        new_text.append(text[last_index:start])

        base = md_path.stem
        mmd_name = f"{base}-mermaid-{i}.mmd"
        mmd_path = assets / mmd_name
        mmd_path.write_text(mermaid_code + "\n", encoding="utf-8")

        svg_name = f"{base}-mermaid-{i}.svg"
        svg_path = assets / svg_name

        if svg_path.exists():
            img_md = f"![diagram]({svg_path.relative_to(md_path.parent)})\n\n"
        else:
            img_md = f"[Mermaid source: {mmd_name}]({mmd_path.relative_to(md_path.parent)})\n\n"

        details = (
            "<details>\n"
            "<summary>Mermaid source (editable)</summary>\n\n"
            "```mermaid\n"
            f"{mermaid_code}\n"
            "```\n"
            "</details>\n\n"
        )

        new_text.append(img_md)
        new_text.append(details)
        changed = True
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
            if process_file(md):
                print("Updated:", md)
                processed.append(md)
        except Exception as e:
            print("Error processing", md, e)

    print(f"Done. Processed {len(processed)} files.")


if __name__ == "__main__":
    main()
